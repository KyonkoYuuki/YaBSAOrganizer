from yabsa.panels.types import BasePanel, MAX_UINT16

from pyxenoverse.bsa.types.type12 import Type12

class Type12Panel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False)


        self.eepk_type = self.add_single_selection_entry(self.entry_page, 'EEPK Type', majorDimension=2, choices=Type12.description_choices())
        self.skill_id = self.add_num_entry(self.entry_page, 'Skill ID', max=MAX_UINT16)
        self.effect_id = self.add_num_entry(self.entry_page, 'Effect ID?')
        self.i_12 = self.add_hex_entry(self.entry_page, 'I_12')
        self.f_16 = self.add_float_entry(self.entry_page, 'F_16')


