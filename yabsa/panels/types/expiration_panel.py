from yabsa.panels.types import BasePanel, MAX_UINT16


class ExpirationPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False, has_duration=False)
        self.i_00 = self.add_hex_entry(self.entry_page, 'I_00', max=MAX_UINT16)
        self.i_02 = self.add_hex_entry(self.entry_page, 'I_02', max=MAX_UINT16)
        self.i_04 = self.add_hex_entry(self.entry_page, 'I_04', max=MAX_UINT16)
        self.i_06 = self.add_hex_entry(self.entry_page, 'I_06', max=MAX_UINT16)
