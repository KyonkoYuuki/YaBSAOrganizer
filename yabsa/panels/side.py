import re
import sys

from pubsub import pub
import wx


from pyxenoverse.bsa.sub_entry import ITEM_TYPES

from yabsa.panels.types.entry_panel import EntryPanel
from yabsa.panels.types.collision_panel import CollisionPanel
from yabsa.panels.types.expiration_panel import ExpirationPanel
from yabsa.panels.types.entry_passing_panel import EntryPassingPanel
from yabsa.panels.types.movement_panel import MovementPanel
from yabsa.panels.types.type2_panel import Type2Panel
from yabsa.panels.types.hitbox import HitboxPanel
from yabsa.panels.types.deflection_panel import DeflectionPanel
from yabsa.panels.types.effect_panel import EffectPanel
from yabsa.panels.types.sound import SoundPanel
from yabsa.panels.types.type8_panel import Type8Panel
from yabsa.panels.types.type12_panel import Type12Panel


RE_PATTERN = re.compile(r".*'(.*[.])*(.*)'.*")


class SidePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer()
        self.root = parent
        self.panels = {}
        self.current_panel = None

        # Entry
        entry_panel = EntryPanel(self)
        entry_panel.Hide()
        sizer.Add(entry_panel, 1, wx.ALL | wx.EXPAND, 10)

        self.panels = {'Entry': entry_panel}
        # Subtypes
        for bsa_type in ITEM_TYPES.values():
            name = re.match(RE_PATTERN, str(bsa_type)).group(2)
            panel_class = getattr(sys.modules[__name__], name + 'Panel')

            panel = panel_class(self, self.root, name, bsa_type)
            panel.Hide()
            self.panels[name] = panel
            sizer.Add(panel, 1, wx.ALL | wx.EXPAND, 10)

        pub.subscribe(self.load_entry, 'load_entry')
        pub.subscribe(self.hide_panels, 'hide_panels')

        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def show_panel(self, panel, item, entry):
        if self.current_panel != panel:
            if self.current_panel:
                self.current_panel.Hide()
            self.current_panel = panel
            self.current_panel.Show()
            self.current_panel.Layout()
            self.Layout()
        self.current_panel.load_entry(item, entry)

    def hide_panels(self):
        for panel in self.panels.values():
            panel.Hide()
        pub.sendMessage('clear_focus')
        self.current_panel = None
        self.Layout()

    def load_entry(self, item, entry):
        entry_type = type(entry)
        if entry_type.__name__ == 'Entry' \
                or entry_type.__name__ == 'Collision' \
                or entry_type.__name__ == 'Expiration' \
                or entry_type in ITEM_TYPES.values():
            name = entry_type.__name__
            self.show_panel(self.panels[name], item, entry)
        else:
            self.hide_panels()


