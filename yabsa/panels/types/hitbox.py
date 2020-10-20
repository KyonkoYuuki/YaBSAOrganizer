from yabsa.panels.types import BasePanel, MAX_UINT16


class HitboxPanel(BasePanel):
    def __init__(self, *args):
        BasePanel.__init__(self, *args)
        self.i_00 = self.add_hex_entry(self.unknown_page, 'I_00', max=MAX_UINT16)
        self.i_02 = self.add_hex_entry(self.unknown_page, 'I_02', max=MAX_UINT16)
        self.i_04 = self.add_hex_entry(self.unknown_page, 'I_04', max=MAX_UINT16)
        self.i_06 = self.add_hex_entry(self.unknown_page, 'I_06', max=MAX_UINT16)
        self.position_x = self.add_float_entry(self.entry_page, 'Position X')
        self.position_y = self.add_float_entry(self.entry_page, 'Position Y')
        self.position_z = self.add_float_entry(self.entry_page, 'Position Z')
        self.hitbox_scale = self.add_float_entry(self.entry_page, 'Hitbox Scale')
        self.f_24 = self.add_float_entry(self.unknown_page, 'F_24')
        self.f_28 = self.add_float_entry(self.unknown_page, 'F_28')
        self.f_32 = self.add_float_entry(self.unknown_page, 'F_32')
        self.f_36 = self.add_float_entry(self.unknown_page, 'F_36')
        self.f_40 = self.add_float_entry(self.unknown_page, 'F_40')
        self.amount = self.add_float_entry(self.entry_page, 'Amount')
        self.lifetime = self.add_num_entry(self.entry_page, 'Lifetime', max=MAX_UINT16)
        self.i_50 = self.add_hex_entry(self.unknown_page, 'I_50', max=MAX_UINT16)
        self.i_52 = self.add_hex_entry(self.unknown_page, 'I_52', max=MAX_UINT16)
        self.i_54 = self.add_hex_entry(self.unknown_page, 'I_54', max=MAX_UINT16)
        self.i_56 = self.add_hex_entry(self.unknown_page, 'I_56', max=MAX_UINT16)
        self.bdm_first_hit_id = self.add_num_entry(self.entry_page, 'BDM First Hit ID', max=MAX_UINT16)
        self.bdm_multiple_hits_id = self.add_num_entry(self.entry_page, 'BDM Multiple Hits ID', max=MAX_UINT16)
        self.bdm_last_hit_id = self.add_num_entry(self.entry_page, 'BDM Last Hit ID', max=MAX_UINT16)
