from yabsa.panels.types import BasePanel


class Type12Panel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False)
        self.f_00 = self.add_float_entry(self.entry_page, 'F_00')
        self.eepk_type = self.add_single_selection_entry(self.entry_page, 'EEPK Type', majorDimension=2, choices={
            'None': 65535,
            'Common': 0,
            'Stage BG': 1,
            'Character': 2,
            'Awoken Skill': 3,
            'Super Skill': 5,
            'Ultimate Skill': 6,
            'Evasive Skill': 7,
            'Ki Blast Skill': 9,
            'Stage': 11
        })
        self.skill_id = self.add_num_entry(self.entry_page, 'Skill ID')
        self.i_12 = self.add_hex_entry(self.entry_page, 'I_12')
        self.f_16 = self.add_float_entry(self.entry_page, 'F_16')
