from yabsa.panels.types import BasePanel, MAX_UINT16
from pyxenoverse.bsa.types.sound import Sound

class SoundPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)
        self.acb_file = self.add_single_selection_entry(self.entry_page, 'ACB File', choices=Sound.description_choices())
        self.i_02 = self.add_hex_entry(self.unknown_page, 'I_02', max=MAX_UINT16)
        self.cue_id = self.add_num_entry(self.entry_page, 'Cue ID', max=MAX_UINT16)
        self.i_06 = self.add_hex_entry(self.unknown_page, 'I_06', max=MAX_UINT16)
