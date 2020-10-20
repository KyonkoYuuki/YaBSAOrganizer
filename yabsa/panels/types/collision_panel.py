from yabsa.panels.types import BasePanel, MAX_UINT16


class CollisionPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, has_duration=False)
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
            'Stage': 11,
        })
        self.skill_id = self.add_num_entry(self.entry_page, 'Skill ID', max=MAX_UINT16)
        self.effect_id = self.add_num_entry(self.entry_page, 'Effect ID')
        self.i_08 = self.add_hex_entry(self.unknown_page, 'I_08')
        self.i_12 = self.add_hex_entry(self.unknown_page, 'I_12')
        self.i_16 = self.add_hex_entry(self.unknown_page, 'I_16')
        self.i_20 = self.add_hex_entry(self.unknown_page, 'I_20')
