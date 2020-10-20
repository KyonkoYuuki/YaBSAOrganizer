from yabsa.panels.types import BasePanel, MAX_UINT16


class EffectPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)
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
        self.skill_id = self.add_num_entry(self.entry_page, 'Skill ID', max=MAX_UINT16)
        self.effect_id = self.add_num_entry(self.entry_page, 'Effect ID', max=MAX_UINT16)
        self.i_06 = self.add_hex_entry(self.unknown_page, 'I_06', max=MAX_UINT16)
        self.effect_switch = self.add_single_selection_entry(self.entry_page, 'Effect Switch', choices={
            'On': 0,
            'Off': 1,
        })
        self.i_10 = self.add_hex_entry(self.unknown_page, 'I_10', max=MAX_UINT16)
        self.position_x = self.add_float_entry(self.entry_page, 'Position X')
        self.position_y = self.add_float_entry(self.entry_page, 'Position Y')
        self.position_z = self.add_float_entry(self.entry_page, 'Position Z')
