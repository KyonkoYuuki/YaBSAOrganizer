import wx

from yabsa.panels.types import BasePanel, MAX_UINT32


class MovementPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)
        self.motion_flags = self.add_hex_entry(self.entry_page, "Motion Flags", max=MAX_UINT32)
        self.speed_x = self.add_float_entry(self.entry_page, "Speed X")
        self.speed_y = self.add_float_entry(self.entry_page, "Speed Y")
        self.speed_z = self.add_float_entry(self.entry_page, "Speed Z")
        self.f_16 = self.add_float_entry(self.unknown_page, 'F_12')
        self.acceleration_x = self.add_float_entry(self.entry_page, "Acceleration X")
        self.acceleration_y = self.add_float_entry(self.entry_page, "Acceleration Y")
        self.acceleration_z = self.add_float_entry(self.entry_page, "Acceleration Z")
        self.falloff_strength = self.add_float_entry(self.entry_page, "Falloff Strength")
        self.spread_x = self.add_float_entry(self.entry_page, "Spread Direction X")
        self.spread_y = self.add_float_entry(self.entry_page, "Spread Direction Y")
        self.spread_z = self.add_float_entry(self.entry_page, "Spread Direction Z")
