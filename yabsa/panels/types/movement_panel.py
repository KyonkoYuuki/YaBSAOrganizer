import wx

from yabsa.panels.types import BasePanel, MAX_UINT32


class MovementPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)
        self.motion_flags = self.add_multiple_selection_entry(self.entry_page, 'Motion Flags', cols=4, majorDimension=3,choices=[
            ('Options #1', None, True),
            ('Options #2', [
                 'Unknown (0x1)',
                 'Unknown (0x2)',
                 'Unknown (0x4)',
                 'Unknown (0x8)'
             ],
             True),
            ('Options #3', [
                'Unknown (0x1)',
                'Free Movement?',
                'Unknown (0x4)',
                'Unknown (0x8)'
            ],
             True),
            ('Options #4', [
                'Unknown (0x1)',
                'Opponent Tracking',
                'Unknown (0x4)',
                'Unknown (0x8)'
            ], True),
            ('Options #5', [
                'Unknown (0x1)',
                'Unknown (0x2)',
                'Unknown (0x4)',
                'Unknown (0x8)'
            ], True),
            ('Options #6', [
                'Unknown (0x1)',
                'Unknown (0x2)',
                'Unknown (0x4)',
                'Unknown (0x8)'
            ], True),
            ('Options #7', [
                'Unknown (0x1)',
                'Unknown (0x2)',
                'Unknown (0x4)',
                'Unknown (0x8)'
            ], True),
            ('Options #8', [
                'Unknown (0x1)',
                'Unknown (0x2)',
                'Unknown (0x4)',
                'Unknown (0x8)'
            ], True)
        ])

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
