import wx
from pubsub import pub
from pyxenoverse.gui.ctrl.hex_ctrl import HexCtrl
from pyxenoverse.gui.ctrl.split_hex_ctrl import SplitHexCtrl
from yabsa.panels.types import add_entry, Page
from yabsa.panels.types import MAX_UINT16


class EntryPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.item = None
        self.entry = None

        self.notebook = wx.Notebook(self)
        self.entry_page = Page(self.notebook)
        self.unknown_page = Page(self.notebook)
        self.notebook.AddPage(self.entry_page, 'Entry')
        self.notebook.AddPage(self.unknown_page, 'Unknown')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 10)

        self.impact_properties = self.add_split_hex_entry(self.entry_page, 'Impact Properties', bytes=1)
        self.lifetime = self.add_num_entry(self.entry_page, 'Lifetime', MAX_UINT16)
        self.expires = self.add_num_entry(self.entry_page, 'Expires', MAX_UINT16)
        self.impact_projectile = self.add_num_entry(self.entry_page, 'Impact Projectile', MAX_UINT16)
        self.impact_enemy = self.add_num_entry(self.entry_page, 'Impact Enemy', MAX_UINT16)
        self.impact_ground = self.add_num_entry(self.entry_page, 'Impact Ground', MAX_UINT16)

        self.i_00 = self.add_hex_entry(self.unknown_page, 'I_00')
        self.i_17 = self.add_hex_entry(self.unknown_page, 'I_17', max=255)
        self.i_18 = self.add_hex_entry(self.unknown_page, 'I_18')
        self.i_24 = self.add_hex_entry(self.unknown_page, 'I_24', max=MAX_UINT16)
        self.i_40 = self.add_hex_entry(self.unknown_page, 'I_40')
        self.i_44 = self.add_hex_entry(self.unknown_page, 'I_44')
        self.i_48 = self.add_hex_entry(self.unknown_page, 'I_48')

        self.Bind(wx.EVT_TEXT, self.save_entry)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def __getitem__(self, item):
        return self.__getattribute__(item)

    @add_entry
    def add_num_entry(self, panel, _, *args, **kwargs):
        if 'size' not in kwargs:
            kwargs['size'] = (150, -1)
        kwargs['min'], kwargs['max'] = 0, 65535
        return wx.SpinCtrl(panel, *args, **kwargs)

    @add_entry
    def add_hex_entry(self, panel, _, *args, **kwargs):
        return HexCtrl(panel, *args, **kwargs)

    @add_entry
    def add_split_hex_entry(self, panel, _, *args, **kwargs):
        return SplitHexCtrl(panel, *args, **kwargs)

    def load_entry(self, item, entry):
        self.item = item
        for name in entry.__fields__:
            try:
                self[name].SetValue(entry[name])
            except AttributeError:
                continue
        self.entry = entry

    def save_entry(self, _):
        if self.entry is None:
            return
        for name in self.entry.__fields__:
            try:
                control = self[name]
            except AttributeError:
                continue
            self.entry[name] = control.GetValue()

        pub.sendMessage('update_entry', item=self.item, entry=self.entry)
