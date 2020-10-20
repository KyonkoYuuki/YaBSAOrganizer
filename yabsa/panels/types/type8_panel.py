from yabsa.panels.types import BasePanel


class Type8Panel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False)
        self.i_00 = self.add_hex_entry(self.entry_page, 'I_00')
        self.i_04 = self.add_hex_entry(self.entry_page, 'I_04')
        self.i_08 = self.add_hex_entry(self.entry_page, 'I_08')
        self.i_12 = self.add_hex_entry(self.entry_page, 'I_12')
        self.i_16 = self.add_hex_entry(self.entry_page, 'I_16')
        self.i_20 = self.add_hex_entry(self.entry_page, 'I_20')
