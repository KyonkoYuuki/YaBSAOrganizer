from yabsa.panels.types import BasePanel, MAX_UINT16


class Type10Panel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False)
        self.skill_id = self.add_num_entry(self.entry_page, 'Skill ID?', max=MAX_UINT16)
        self.i_02 = self.add_hex_entry(self.entry_page, 'I_02', max=MAX_UINT16)
        self.i_04 = self.add_hex_entry(self.entry_page, 'I_04', max=MAX_UINT16)
