from yabsa.panels.types import BasePanel, MAX_UINT16


class EntryPassingPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)

        self.i_00 = self.add_unknown_hex_entry(self.entry_page, 'First Condition', max=MAX_UINT16,
                                                         knownValues={
                                                             0x0: "Unknown",
                                                             0x4: "Pass When Attack Hits?",
                                                             0x5: "BAC Related Pass?"

                                                         })


        self.main_condition = self.add_multiple_selection_entry(self.entry_page, 'Second Condition Options', choices=[
            ('Options #1', [
                'Unknown (0x1)',
                'Unknown (0x2)',
                "Unknown (0x4)",
                'Unknown (0x8)'
            ], True),
            ('Options #2', None, True),
            ('Options #3', [
                'Unknown (0x1)',
                'Unknown (0x2)',
                "Unknown (0x4)",
                'BAC Condition from System (0x8)'
            ], True),
        ])


        self.bsa_entry_id = self.add_num_entry(self.entry_page, 'BSA Entry ID', max=MAX_UINT16)
        self.jump_to_bac_entry_id = self.add_num_entry(self.entry_page, 'Jump to BAC entry ID?', max=MAX_UINT16)
        self.bac_condition = self.add_float_entry(self.entry_page, 'BAC Condition')
        self.f_12 = self.add_float_entry(self.unknown_page, 'F_12')
