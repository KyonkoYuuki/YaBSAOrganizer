from yabsa.panels.types import BasePanel


class Type13Panel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False)

        self.i_00 = self.add_hex_entry(self.entry_page, 'i_00')
        self.i_02 = self.add_hex_entry(self.entry_page, 'i_02')
        self.power = self.add_float_entry(self.entry_page, 'Power?')
        self.f_08 = self.add_float_entry(self.entry_page, 'f_08')
        self.i_12 = self.add_hex_entry(self.entry_page, 'i_12')
        self.f_16 = self.add_float_entry(self.entry_page, 'f_16')
        self.i_20 = self.add_hex_entry(self.entry_page, 'i_20')
        self.i_24 = self.add_hex_entry(self.entry_page, 'i_24')
        self.i_28 = self.add_hex_entry(self.entry_page, 'i_28')

