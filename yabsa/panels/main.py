from functools import partial
import pickle

import wx
from pubsub import pub

from pyxenoverse.bsa.entry import Entry
from pyxenoverse.bsa.collision import Collision
from pyxenoverse.bsa.expiration import Expiration
from pyxenoverse.bsa.sub_entry import SubEntry, ITEM_TYPES
from pyxenoverse.gui import get_first_item, get_next_item
from pyxenoverse.gui.ctrl.multiple_selection_box import MultipleSelectionBox
from pyxenoverse.gui.ctrl.single_selection_box import SingleSelectionBox
from pyxenoverse.gui.ctrl.unknown_hex_ctrl import UnknownHexCtrl
from pyxenoverse.gui.file_drop_target import FileDropTarget

from yabsa.dlg.new import NewEntryDialog


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.focus = None
        self.bsa = None
        self.cdo = None
        self.refresh = True

        self.entry_list = wx.TreeCtrl(self, style=wx.TR_MULTIPLE | wx.TR_HAS_BUTTONS | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_LINES_AT_ROOT | wx.TR_HIDE_ROOT)
        self.entry_list.SetDropTarget(FileDropTarget(self, "load_bsa"))
        self.entry_list.Bind(wx.EVT_TREE_ITEM_MENU, self.on_right_click)
        self.entry_list.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_select)
        self.cdo = wx.CustomDataObject("BSAEntry")

        self.Bind(wx.EVT_MENU, self.on_open, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_save, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.on_delete, id=wx.ID_DELETE)
        self.Bind(wx.EVT_MENU, self.on_copy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.on_paste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU, self.on_add_copy, id=wx.ID_ADD)
        self.Bind(wx.EVT_MENU, self.on_new, id=wx.ID_NEW)

        accelerator_table = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('c'), wx.ID_COPY),
            (wx.ACCEL_CTRL, ord('v'), wx.ID_PASTE),
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('v'), wx.ID_ADD),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_DELETE),
        ])
        self.entry_list.SetAcceleratorTable(accelerator_table)

        # Publishers
        pub.subscribe(self.update_entry, 'update_entry')
        pub.subscribe(self.update_item, 'update_item')
        pub.subscribe(self.on_select, 'on_select')
        pub.subscribe(self.reindex, 'reindex')
        pub.subscribe(self.set_focus, 'set_focus')
        pub.subscribe(self.clear_focus, 'clear_focus')

        # Use some sizers to see layout options
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.entry_list, 1, wx.ALL | wx.EXPAND, 10)

        # Layout sizers
        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def enable_selected(self, menu_item, single=True, entry=None):
        selected = self.entry_list.GetSelections()
        if not selected:
            menu_item.Enable(False)
        elif single and len(selected) > 1:
            menu_item.Enable(False)
        elif entry:
            data = self.entry_list.GetItemData(selected[0])
            if data.get_readable_name() != entry.get_readable_name():
                menu_item.Enable(False)

    def on_right_click(self, _):
        menu = wx.Menu()
        sub_entry_menu = wx.Menu()
        add = menu.Append(wx.ID_NEW, "&Add Entry", "Add BSA Entry")
        self.enable_selected(add)
        menu.AppendSubMenu(sub_entry_menu, "Add &Subentry")
        for bsa_value, bsa_type in ITEM_TYPES.items():
            name = bsa_type.__name__
            if bsa_value < 0:
                name += " (After Effects)"
            sub_entry_item = sub_entry_menu.Append(-1, name)
            self.enable_selected(sub_entry_item)
            self.Bind(wx.EVT_MENU, partial(self.on_add_item, bsa_value=bsa_value), sub_entry_item)
        delete = menu.Append(wx.ID_DELETE, "Delete\tDel", "&Delete entry(s)")
        self.enable_selected(delete, single=False)
        copy = menu.Append(wx.ID_COPY, "Copy\tCtrl+C", "&Copy entry(s)")
        self.enable_selected(copy)
        menu.AppendSeparator()
        # Paste options
        paste_data = self.get_paste_data(self.entry_list.GetSelections(), False)
        if not paste_data:
            paste = menu.Append(-1, "<no copied item found>")
            paste.Enable(False)
        else:
            name = paste_data.get_readable_name()
            title = menu.Append(-1, "Copied " + name)
            title.Enable(False)
            paste = menu.Append(wx.ID_PASTE, f"&Paste {name}\tCtrl+V")
            self.enable_selected(paste, entry=paste_data)
            add_copy = menu.Append(-1, f"Add {name} Copy\tCtrl+Shift+V")
            self.enable_selected(add_copy)
            self.Bind(wx.EVT_MENU, self.on_add_copy, add_copy)

        self.PopupMenu(menu)
        menu.Destroy()

    def on_open(self, _):
        pub.sendMessage('open_bsa', e=None)

    def on_save(self, _):
        pub.sendMessage('save_bsa', e=None)

    def expand_parents(self, item):
        root = self.entry_list.GetRootItem()
        parent = self.entry_list.GetItemParent(item)
        while parent != root:
            self.entry_list.Expand(parent)
            parent = self.entry_list.GetItemParent(parent)

    def select_item(self, item):
        self.entry_list.UnselectAll()
        self.entry_list.SelectItem(item)
        self.expand_parents(item)
        if not self.entry_list.IsVisible(item):
            self.entry_list.ScrollTo(item)

    def get_selected_root_nodes(self):
        selected = self.entry_list.GetSelections()
        if not selected:
            return []
        root = self.entry_list.GetRootItem()

        nodes = []
        for item in selected:
            parent = self.entry_list.GetItemParent(item)
            while parent != root and parent.IsOk():
                if parent in selected:
                    break
                parent = self.entry_list.GetItemParent(parent)
            if parent == root:
                nodes.append(item)
        return nodes

    def on_select(self, _):
        if not self.entry_list or not self.refresh:
            return
        selected = self.entry_list.GetSelections()
        if len(selected) != 1:
            pub.sendMessage('hide_panels')
            return
        entry = self.entry_list.GetItemData(selected[0])
        pub.sendMessage('load_entry', item=selected[0], entry=entry)

    def update_entry(self, item, entry):
        self.entry_list.SetItemText(item, f'{entry.index}: Entry')

    def update_item(self, item, entry):
        self.refresh = False
        parent = self.entry_list.GetItemParent(item)
        self.entry_list.Delete(item)
        child = self.entry_list.GetFirstChild(parent)[0]
        index = 0
        while child.IsOk():
            if self.entry_list.GetItemData(child).start_time > entry.start_time:
                new_item = self.entry_list.InsertItem(
                    parent, index, str(entry.start_time), data=entry)
                break
            child = self.entry_list.GetNextSibling(child)
            index += 1
        else:
            new_item = self.entry_list.AppendItem(
                parent, f'{entry.index}: {entry.start_time}', data=entry)
        self.select_item(new_item)
        self.refresh = True
        self.on_select(None)
        return new_item

    def build_tree(self):
        self.entry_list.DeleteAllItems()
        self.entry_list.Refresh()
        self.entry_list.AddRoot("Entries")
        for i, entry in enumerate(self.bsa.entries):
            entry_item = self.entry_list.AppendItem(
                self.entry_list.GetRootItem(), f'{entry.index}: Entry', data=entry)
            self.build_entry_tree(entry_item, entry)

    def build_entry_tree(self, entry_item, entry):
        if entry.collisions:
            collisions_item = self.entry_list.AppendItem(entry_item, f'Collision (After Effects)', data=entry.collisions)
            self.build_collision_tree(collisions_item, entry.collisions)

        if entry.expirations:
            expirations_item = self.entry_list.AppendItem(entry_item, f'Expiration (After Effects)', data=entry.expirations)
            self.build_expiration_tree(expirations_item, entry.expirations)

        for sub_entry in entry.sub_entries:
            sub_entry_item = self.entry_list.AppendItem(
                entry_item, f'{sub_entry.type}: {sub_entry.get_type_name()}', data=sub_entry)
            self.build_sub_entry_tree(sub_entry_item, sub_entry)

    def build_collision_tree(self, collisions_item, collisions):
        for n, collision in enumerate(collisions):
            self.entry_list.AppendItem(collisions_item, f'{n}', data=collision)

    def build_expiration_tree(self, expirations_item, expirations):
        for n, expiration in enumerate(expirations):
            self.entry_list.AppendItem(expirations_item, f'{n}', data=expiration)

    def build_sub_entry_tree(self, sub_entry_item, sub_entry):
        for item in sub_entry.items:
            self.entry_list.AppendItem(sub_entry_item, str(item.start_time), data=item)

    def get_current_entry_ids(self):
        entry_ids = []
        item, _ = get_first_item(self.entry_list)
        while item.IsOk():
            data = self.entry_list.GetItemData(item)
            entry_ids.append(data.index)
            item = self.entry_list.GetNextSibling(item)
        return entry_ids

    def reindex(self):
        for i, entry in enumerate(self.bsa.entries):
            # entry.flags = entry.flags & 0xF if len(entry.sub_entries) > 0 else (entry.flags & 0x0F) | 0x80000000
            entry.sub_entries.sort(key=lambda n: n.type)
            for j, sub_entry in enumerate(entry.sub_entries):
                sub_entry.index = j
                sub_entry.items.sort(key=lambda n: n.start_time)
                for k, item in enumerate(sub_entry.items):
                    item.index = k

        item, _ = get_first_item(self.entry_list)

        # Fix tree names
        while item.IsOk():
            data = self.entry_list.GetItemData(item)
            name = data.get_name() if data else None
            if name == 'Entry':
                self.entry_list.SetItemText(item, f'{data.index}: Entry')
            elif name == 'SubEntry':
                self.entry_list.SetItemText(item, f'{data.type}: {data.get_type_name()}')
                sub_entry = self.entry_list.GetItemData(item)
                for entry in sub_entry.items:
                    item = get_next_item(self.entry_list, item)
                    self.entry_list.SetItemData(item, entry)
                    self.entry_list.SetItemText(item, str(entry.start_time))
            item = get_next_item(self.entry_list, item)

    def get_entry_item_pair(self, entry):
        return entry, self.entry_list.GetItemData(entry)

    def get_parent_bsa_entry(self, bsa_entry):
        if bsa_entry:
            return self.get_entry_item_pair(bsa_entry)
        bsa_entry = self.entry_list.GetSelections()[0]
        while bsa_entry.IsOk():
            data = self.entry_list.GetItemData(bsa_entry)
            name = data.get_name() if data else None
            if name == 'Entry':
                return self.get_entry_item_pair(bsa_entry)
            bsa_entry = self.entry_list.GetItemParent(bsa_entry)
        else:
            return None, None

    def get_previous_index(self, entry_id):
        item, _ = get_first_item(self.entry_list)
        tree_index = 0
        while item.IsOk():
            data = self.entry_list.GetItemData(item)
            if data.index > entry_id:
                break
            tree_index += 1
            item = self.entry_list.GetNextSibling(item)
        return tree_index

    def add_bsa_entry(self, entry):
        root = self.entry_list.GetRootItem()
        prev = self.get_previous_index(entry.index)
        item = self.entry_list.InsertItem(root, prev, f'{entry.index}: Entry', data=entry)
        self.entry_list.SelectItem(item)
        self.on_select(None)
        return item

    def add_sub_entry(self, bsa_value, bsa_entry=None):
        bsa_entry, data = self.get_parent_bsa_entry(bsa_entry)
        if not bsa_entry or not data:
            return None, None

        # Try to find the sub_entry first
        item = self.entry_list.GetFirstChild(bsa_entry)[0]
        while item.IsOk():
            sub_entry = self.entry_list.GetItemData(item)
            if sub_entry and sub_entry.type == bsa_value:
                return item, sub_entry
            item = self.entry_list.GetNextSibling(item)

        # If not found, create a new one
        new_sub_entry = SubEntry(0)
        new_sub_entry.type = bsa_value
        data.sub_entries.append(new_sub_entry)
        data.sub_entries.sort(key=lambda n: n.type)

        # Reindex real fast
        for i, sub_entry in enumerate(data.sub_entries):
            sub_entry.index = i

        # Try to insert it into the tree at the right place
        max_index = new_sub_entry.index
        if data.collisions:
            max_index += 1
        if data.expirations:
            max_index += 1
        index = 0
        item = self.entry_list.GetFirstChild(bsa_entry)[0]
        for i in range(max_index):
            if not item.IsOk():
                break
            item = self.entry_list.GetNextSibling(item)
            index += 1
        new_item = self.entry_list.InsertItem(
            bsa_entry, index, f'{new_sub_entry.type}: {new_sub_entry.get_type_name()}', data=new_sub_entry)
        return new_item, new_sub_entry

    def add_collision(self, copied_entry=None, bsa_entry=None):
        if copied_entry and not isinstance(copied_entry, Collision):
            with wx.MessageDialog(self, f"Data format doesn't match Collision type") as dlg:
                dlg.ShowModal()
            return

        # Get BSA entry
        bsa_entry, data = self.get_parent_bsa_entry(bsa_entry)
        if not bsa_entry or not data:
            return

        # Try to find the collision tree
        item = self.entry_list.GetFirstChild(bsa_entry)[0]
        sub_entry = None
        while item.IsOk():
            text = self.entry_list.GetItemText(item)
            if text.startswith("Collision"):
                sub_entry = item
                break
            item = self.entry_list.GetNextSibling(item)

        # Create collision tree if it doesn't exist
        if not sub_entry:
            sub_entry = self.entry_list.InsertItem(bsa_entry, 0, "Collision (After Effects)", data=data.collisions)

        # Create new collision
        collision = Collision()
        collision.paste(copied_entry)

        # Add it collision list
        data.collisions.append(collision)

        # Add it to tree
        new_item = self.entry_list.AppendItem(sub_entry, f'{len(data.collisions) - 1}', data=collision)
        return new_item, collision

    def add_expiration(self, copied_entry=None, bsa_entry=None):
        if copied_entry and not isinstance(copied_entry, Expiration):
            with wx.MessageDialog(self, f"Data format doesn't match Expiration type") as dlg:
                dlg.ShowModal()
            return

        # Get BSA entry
        bsa_entry, data = self.get_parent_bsa_entry(bsa_entry)
        if not bsa_entry or not data:
            return

        # Try to find the collision tree
        item = self.entry_list.GetFirstChild(bsa_entry)[0]
        first_text = self.entry_list.GetItemText(item)
        sub_entry = None
        while item.IsOk():
            text = self.entry_list.GetItemText(item)
            if text.startswith("Expiration"):
                sub_entry = item
                break
            item = self.entry_list.GetNextSibling(item)

        # Create collision tree if it doesn't exist
        if not sub_entry:
            index = 1 if first_text.startswith("Collision") else 0
            sub_entry = self.entry_list.InsertItem(bsa_entry, index, "Expiration (After Effects)", data=data.expirations)

        # Create new expiration
        expiration = Expiration()
        expiration.paste(copied_entry)

        # Add it collision list
        data.expirations.append(expiration)

        # Add it to tree
        new_item = self.entry_list.AppendItem(sub_entry, f'{len(data.expirations) - 1}', data=expiration)
        return new_item, expiration

    def add_item(self, bsa_value, copied_entry=None, bsa_entry=None):
        if copied_entry and bsa_value != copied_entry.type:
            with wx.MessageDialog(self, f"Data format doesn't match '{ITEM_TYPES[bsa_value].__name__}' type") as dlg:
                dlg.ShowModal()
            return

        # Get BSA entry
        bsa_entry, data = self.get_parent_bsa_entry(bsa_entry)
        if not bsa_entry or not data:
            return

        # Get or add sub_entry
        sub_entry, sub_entry_data = self.add_sub_entry(bsa_value, bsa_entry)

        # Create new item
        new_bsa_type = ITEM_TYPES[bsa_value](0)
        new_bsa_type.paste(copied_entry)

        # Add it to sub_entry
        sub_entry_data.items.append(new_bsa_type)
        sub_entry_data.items.sort(key=lambda n: n.start_time)

        # Add to correct place in tree list
        index = 0
        item = self.entry_list.GetFirstChild(sub_entry)[0]
        while item.IsOk():
            if new_bsa_type.start_time <= self.entry_list.GetItemData(item).start_time:
                break
            item = self.entry_list.GetNextSibling(item)
            index += 1
        new_item = self.entry_list.InsertItem(sub_entry, index, '', data=new_bsa_type)
        return new_item, new_bsa_type

    def on_new(self, _):
        if self.bsa is None:
            return
        with NewEntryDialog(self, self.get_current_entry_ids()) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            entry_id = dlg.GetValue()
        self.entry_list.UnselectAll()

        # Add it
        entry = Entry(entry_id)
        item = self.add_bsa_entry(entry)
        pub.sendMessage('set_status_bar', text='Added new entry')
        return item, entry

    def on_add_item(self, _, bsa_value):
        if bsa_value == -2:
            new_item, _ = self.add_collision()
        elif bsa_value == -1:
            new_item, _ = self.add_expiration()
        else:
            new_item, _ = self.add_item(bsa_value)
        self.select_item(new_item)
        self.reindex()
        self.on_select(None)
        pub.sendMessage('set_status_bar', text=f"Added new {ITEM_TYPES[bsa_value].__name__}")

    def on_delete(self, _):
        # Get only the parents and select them.
        selected = self.get_selected_root_nodes()
        if not selected:
            return

        # Loop over and delete
        for item in reversed(selected):
            data = self.entry_list.GetItemData(item)
            if data.get_name() == 'Entry':
                self.bsa.entries.remove(data)
            elif data.get_name() == 'SubEntry':
                parent = self.entry_list.GetItemData(self.entry_list.GetItemParent(item))
                parent.sub_entries.remove(data)
            elif data.get_name() == 'CollisionList':
                parent = self.entry_list.GetItemData(self.entry_list.GetItemParent(item))
                parent.collisions.clear()
            elif data.get_name() == 'ExpirationList':
                parent = self.entry_list.GetItemData(self.entry_list.GetItemParent(item))
                parent.expirations.clear()
            elif data.get_name() == 'Collision':
                parent = self.entry_list.GetItemData(self.entry_list.GetItemParent(item))
                parent.remove(data)
            elif data.get_name() == 'Expiration':
                parent = self.entry_list.GetItemData(self.entry_list.GetItemParent(item))
                parent.remove(data)
            else:
                parent = self.entry_list.GetItemData(self.entry_list.GetItemParent(item))
                parent.items.remove(data)
            self.entry_list.Delete(item)
        self.reindex()
        pub.sendMessage('set_status_bar', text="Deleted successfully")

    def on_copy(self, _):
        selected = self.entry_list.GetSelections()
        if len(selected) > 1:
            with wx.MessageDialog(self, 'Can only copy one entry at a time') as dlg:
                dlg.ShowModal()
            return
        entry = self.entry_list.GetItemData(selected[0])
        self.cdo = wx.CustomDataObject('BSA')
        self.cdo.SetData(pickle.dumps(entry))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(self.cdo)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
        pub.sendMessage('set_status_bar', text=f'Copied {entry.get_readable_name()}')

    def get_paste_data(self, selected, warn=True):
        if len(selected) > 1 and warn:
            with wx.MessageDialog(self, 'Can only paste one entry at a time') as dlg:
                dlg.ShowModal()
            return None
        cdo = wx.CustomDataObject('BSA')
        success = False
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(cdo)
            wx.TheClipboard.Close()
        if success:
            return pickle.loads(cdo.GetData())
        return None

    def on_paste(self, _):
        selected = self.entry_list.GetSelections()
        paste_data = self.get_paste_data(selected)
        if not paste_data:
            return
        item = selected[0]
        expanded = self.entry_list.IsExpanded(item)
        entry = self.entry_list.GetItemData(item)

        if type(paste_data) != type(entry):
            with wx.MessageDialog(self, f"Unable to paste '{paste_data.get_readable_name()}' type "
                                  f"onto '{entry.get_readable_name()}'") as dlg:
                dlg.ShowModal()
            return

        # Paste Data
        entry.paste(paste_data)

        # Delete Children
        child = self.entry_list.GetFirstChild(item)[0]
        while child.IsOk():
            current, child = child, self.entry_list.GetNextSibling(child)
            self.entry_list.Delete(current)
        if not item or not entry:
            return

        # Rebuild Tree
        class_name = entry.get_name()
        if class_name == 'Entry':
            self.build_entry_tree(item, entry)
        elif class_name == 'SubEntry':
            self.build_sub_entry_tree(item, entry)
        elif class_name == 'CollisionList':
            self.build_collision_tree(item, entry)
        elif class_name == 'ExpirationList':
            self.build_expiration_tree(item, entry)
        elif class_name not in ['Collision', 'Expiration']:
            self.update_item(item, entry)

        # Expand item if it was already expanded
        if expanded:
            self.entry_list.Expand(item)
        self.on_select(None)
        self.reindex()
        pub.sendMessage('set_status_bar', text=f"Pasted {paste_data.get_readable_name()}")

    def on_add_copy(self, _):
        selected = self.entry_list.GetSelections()
        paste_data = self.get_paste_data(selected)
        if not paste_data:
            return
        class_name = paste_data.get_name()
        if class_name == 'Entry':
            item, data = self.on_new(None)
            data.paste(paste_data, copy_sub_entries=False)
            self.select_item(item)
            for sub_entry in paste_data.sub_entries:
                for item in sub_entry.items:
                    new_item, new_item_data = self.add_item(item.type, item)
                    new_item_data.paste(item)
            self.entry_list.Expand(item)
        elif class_name == 'SubEntry':
            for item in paste_data.items:
                new_item, new_item_data = self.add_item(item.type, item)
                new_item_data.paste(item)
        elif class_name == 'CollisionList':
            for item in paste_data:
                new_item, new_item_data = self.add_collision(item)
                new_item_data.paste(paste_data)
        elif class_name == 'ExpirationList':
            for item in paste_data:
                new_item, new_item_data = self.add_expiration(item)
                new_item_data.paste(paste_data)
        elif class_name == 'Collision':
            new_item, new_item_data = self.add_collision(paste_data)
            new_item_data.paste(paste_data)
        elif class_name == 'Expiration':
            new_item, new_item_data = self.add_expiration(paste_data)
            new_item_data.paste(paste_data)
        else:
            new_item, new_item_data = self.add_item(paste_data.type, paste_data)
            new_item_data.paste(paste_data)
        self.reindex()
        pub.sendMessage('set_status_bar', text=f"Added {paste_data.get_readable_name()}")

    def set_focus(self, focus):
        if type(focus.GetParent()) in (wx.SpinCtrlDouble, UnknownHexCtrl, SingleSelectionBox, MultipleSelectionBox):
            self.focus = focus.GetParent()
        elif type(focus.GetParent().GetParent()) in (SingleSelectionBox, MultipleSelectionBox):
            self.focus = focus.GetParent().GetParent()
        else:
            self.focus = focus

    def clear_focus(self):
        self.focus = None
