from yabsa.panels.types import BasePanel, MAX_UINT16
from pyxenoverse.bsa.types.screen_effect import ScreenEffect


class ScreenEffectPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args, unknown=False)
        self.bpe_effect_id = self.add_unknown_num_entry(self.entry_page, 'BPE Effect Id',
                                                        knownValues=ScreenEffect.description)
        self.i_02 = self.add_hex_entry(self.entry_page, 'I_02')

        self.i_04 = self.add_hex_entry(self.entry_page, 'I_04')
        self.i_08 = self.add_hex_entry(self.entry_page, 'I_08')
        self.i_12 = self.add_hex_entry(self.entry_page, 'I_12')
        self.i_16 = self.add_hex_entry(self.entry_page, 'I_16')
        self.i_20 = self.add_hex_entry(self.entry_page, 'I_20')
