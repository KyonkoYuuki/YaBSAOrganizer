from yabsa.panels.types import BasePanel, MAX_UINT16


class DeflectionPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False)
        self.i_00 = self.add_hex_entry(self.entry_page, 'I_00')
        self.i_04 = self.add_hex_entry(self.entry_page, 'I_04')
        self.i_08 = self.add_hex_entry(self.entry_page, 'I_08')
        self.f_12 = self.add_float_entry(self.entry_page, 'F_12')
        self.f_16 = self.add_float_entry(self.entry_page, 'F_16')
        self.f_20 = self.add_float_entry(self.entry_page, 'F_20')
        self.i_24 = self.add_hex_entry(self.entry_page, 'I_24')
        self.i_28 = self.add_hex_entry(self.entry_page, 'I_28')
        self.i_32 = self.add_hex_entry(self.entry_page, 'I_32')
        self.i_36 = self.add_hex_entry(self.entry_page, 'I_36')
        self.i_40 = self.add_hex_entry(self.entry_page, 'I_40')
        self.i_44 = self.add_hex_entry(self.entry_page, 'I_44')
        self.i_48 = self.add_hex_entry(self.entry_page, 'I_48', max=MAX_UINT16)
        self.newpower = self.add_num_entry(self.entry_page, 'New Power', max=MAX_UINT16)
        self.i_52 = self.add_hex_entry(self.entry_page, 'I_52', max=MAX_UINT16)
        self.i_54 = self.add_hex_entry(self.entry_page, 'I_54', max=MAX_UINT16)
