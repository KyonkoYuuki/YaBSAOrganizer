from yabsa.panels.types import BasePanel, MAX_UINT16

from pyxenoverse.bsa.types.effect import Effect


class EffectPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)
        self.eepk_type = self.add_single_selection_entry(self.entry_page, 'EEPK Type', majorDimension=2, choices=Effect.description_choices())
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
