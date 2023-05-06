from yabsa.panels.types import BasePanel, MAX_UINT16
from pubsub import pub
from pyxenoverse.gui.ctrl.hex_ctrl import HexCtrl
from pyxenoverse.gui.ctrl.split_hex_ctrl import SplitHexCtrl
from yabsa.panels.types import add_entry, Page
from yabsa.panels.types import MAX_UINT16





class HitboxPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)


        matrix_page = Page(self.notebook)
        self.notebook.InsertPage(1, matrix_page, 'Matrix')


        self.matrix_flags  = self.add_multiple_selection_entry(matrix_page, 'Matrix Flags', choices=[
            ('Matrix Properties', [
                'Enable Min and Max bounds',
                'Unknown (0x2)',
                "Unknown (0x4)",
                'Unknown (0x8)'
            ], True)
        ])
        self.i_02 = self.add_hex_entry(self.unknown_page, 'I_02', max=MAX_UINT16)
        self.i_04 = self.add_hex_entry(self.unknown_page, 'I_04', max=MAX_UINT16)
        self.i_06 = self.add_split_hex_entry(self.entry_page, 'I_06', bytes=2)

        self.position_x = self.add_float_entry(self.entry_page, 'Position X')
        self.position_y = self.add_float_entry(self.entry_page, 'Position Y')
        self.position_z = self.add_float_entry(self.entry_page, 'Position Z')
        self.hitbox_scale = self.add_float_entry(self.entry_page, 'Hitbox Scale')
        self.max_box_x = self.add_float_entry(matrix_page, 'Maximum Box X')
        self.max_box_y = self.add_float_entry(matrix_page, 'Maximum Box Y')
        self.max_box_z = self.add_float_entry(matrix_page, 'Maximum Box Z')
        self.min_box_x = self.add_float_entry(matrix_page, 'Minimum Box X')
        self.min_box_y = self.add_float_entry(matrix_page, 'Minimum Box Y')
        self.min_box_z = self.add_float_entry(matrix_page, 'Minimum Box Z')
        self.amount = self.add_num_entry(self.entry_page, 'Amount')
        self.amount_1 = self.add_hex_entry(self.entry_page, 'Amount_1')
        self.power = self.add_num_entry(self.entry_page, 'Power', max=MAX_UINT16)
        self.i_50 = self.add_hex_entry(self.unknown_page, 'I_50', max=MAX_UINT16)
        self.i_52 = self.add_hex_entry(self.unknown_page, 'I_52', max=MAX_UINT16)
        self.i_54 = self.add_hex_entry(self.unknown_page, 'I_54', max=MAX_UINT16)
        self.i_56 = self.add_hex_entry(self.unknown_page, 'I_56', max=MAX_UINT16)
        self.bdm_first_hit_id = self.add_num_entry(self.entry_page, 'BDM First Hit ID', max=MAX_UINT16)
        self.bdm_multiple_hits_id = self.add_num_entry(self.entry_page, 'BDM Multiple Hits ID', max=MAX_UINT16)
        self.bdm_last_hit_id = self.add_num_entry(self.entry_page, 'BDM Last Hit ID', max=MAX_UINT16)

    @add_entry
    def add_split_hex_entry(self, panel, _, *args, **kwargs):
        return SplitHexCtrl(panel, *args, **kwargs)