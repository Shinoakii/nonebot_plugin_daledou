from ..database.db import DB


QJSQ = 1  # 强健身躯
TSDL = 2  # 天生大力
SSMJ = 3  # 身手敏捷
KRYB = 4  # 快人一步
JHFZ = 5  # 均衡发展
WQHS = 6  # 武器好手
RBHS = 7  # 肉搏好手
DLG = 8  # 第六感
WYS = 9  # 无影手
DHWL = 10  # 大海无量
PCRH = 11  # 皮糙肉厚
LBWB = 12  # 凌波微步
GYZW = 13  # 惯用重物
BZJQ = 14  # 避重就轻
ZS = 15  # 装死
YJJ = 16  # 易筋经
ARYJ = 17  # 黯然一击
XXS = 18  # 修心术
QG = 19  # 气功


class Character:
    def __init__(self, char) -> None:
        self.user_id = char.user_id
        self.base_hp = char.base_hp
        self.level_up_hp = char.level_up_hp
        self.power = char.power
        self.agility = char.agility
        self.speed = char.speed
        self.nick_name = char.nick_name
        self.gender = char.gender
        self.level = char.level
        self.qjsq = 0
        self.tsdl = 0
        self.ssmj = 0
        self.kryb = 0
        self.jhfz = 0
        self.hp = 0
        self.before_fanji_probability = 0  # 打前反击
        self.after_fanji_probability = 0  # 挨打反击
        self.bass_speed_effect = 0  # 基础忽略回合概率
        # 大海无量
        self.dhwl = False
        self.dhwl_value = 0
        # 基础减伤
        self.base_jianshang = 0
        # 分类减伤
        self.small_weaponjs = 0
        self.medium_weaponjs = 0
        self.large_weaponjs = 0
        self.active_skill_js = 0
        # 基础增伤
        self.base_zengshang = 0
        # 分类增伤
        self.base_weaponzs = 0  # 武器增伤
        self.ks_zs = 0  # 空手伤害
        self.small_weaponzs = 0
        self.medium_weaponzs = 0
        self.large_weaponzs = 0
        self.active_skill_zs = 0
        # 命中率
        self.base_hitting_accuracy = 0
        self.small_hitting_accuracy = 0
        self.medium_hitting_accuracy = 0
        self.large_hitting_accuracy = 0
        self.active_skill_hitting_accuracy = 0
        # -------miss-------
        self.base_miss = 0
        self.small_miss = 0
        self.medium_miss = 0
        self.large_miss = 0
        self.active_skill_miss = 0
        self.is_jiasi = False  # 假死
        self.base_fanji_miss = 0
        # -------基础吸血-------
        self.base_absorb = 0
        # 技能暴击
        self.active_skill_crit = 0
        self.set_char_init_att(char)
        self.get_final_att()

    def set_char_init_att(self, char):
        result = DB.get_user_ps_skills_info(char)
        for r in result:
            if r.skill_group_id == QJSQ:
                self.qjsq += r.buff_value
            if r.skill_group_id == TSDL:
                self.tsdl = 1
            if r.skill_group_id == SSMJ:
                self.ssmj = 1
            if r.skill_group_id == KRYB:
                self.kryb = 1
            if r.skill_group_id == JHFZ:
                self.jhfz = 1
            if r.skill_group_id == WQHS:
                self.base_weaponzs += r.buff_value
            if r.skill_group_id == RBHS:
                self.ks_zs += r.buff_value
            if r.skill_group_id == DLG:
                self.after_fanji_probability += r.buff_value
            if r.skill_group_id == WYS:
                self.bass_speed_effect += r.buff_value
            if r.skill_group_id == DHWL:
                self.dhwl = True
                self.dhwl_value += r.buff_value
            if r.skill_group_id == PCRH:
                self.base_jianshang += r.buff_value
            if r.skill_group_id == LBWB:
                self.base_miss += r.buff_value
            if r.skill_group_id == GYZW:
                self.large_weaponzs += r.buff_value
            if r.skill_group_id == BZJQ:
                self.small_weaponzs += r.buff_value
                self.medium_weaponzs += r.buff_value
                self.large_miss += r.buff_value
            if r.skill_group_id == ZS:
                self.is_jiasi = True
            if r.skill_group_id == YJJ:
                self.active_skill_zs += r.buff_value
            if r.skill_group_id == ARYJ:
                self.active_skill_crit += r.buff_value
            if r.skill_group_id == XXS:
                self.active_skill_hitting_accuracy += r.buff_value
            if r.skill_group_id == QG:
                self.active_skill_js += r.buff_value

    def get_final_att(self):
        self.hp = int(self.base_hp + self.level_up_hp + (self.base_hp + self.qjsq) * 0.2) * 20
        self.power = int(self.power + (self.power / 2 + 3) * self.tsdl + (self.power / 5 + 1) * self.jhfz)
        self.agility = int(self.agility + (self.agility / 2 + 3) * self.ssmj + (self.agility / 5 + 1) * self.jhfz)
        self.speed = int(self.speed + (self.speed / 2 + 3) * self.kryb + (self.speed / 5 + 1) * self.jhfz)
