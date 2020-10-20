from yabsa.panels.types import BasePanel, MAX_UINT16


class EntryPassingPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)
        self.i_00 = self.add_hex_entry(self.unknown_page, 'I_00', max=MAX_UINT16)
        self.main_condition = self.add_unknown_hex_entry(self.entry_page, 'Main Condition', max=MAX_UINT16, knownValues={
            0x0: "Pass without BAC Condition",
            0x8: "Pass with TransformControl"
        })
        self.bsa_entry_id = self.add_num_entry(self.entry_page, 'BSA Entry ID', max=MAX_UINT16)
        self.i_06 = self.add_hex_entry(self.unknown_page, 'I_06', max=MAX_UINT16)
        self.bac_condition = self.add_float_entry(self.entry_page, 'BAC Condition')
        self.f_12 = self.add_float_entry(self.unknown_page, 'F_12')
