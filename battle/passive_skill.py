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


class PassiveSkill:
    def __init__(self, skill) -> None:
        self.id = skill.id
        self.ps_name = skill.ps_name
        self.ps_lv = skill.ps_lv
        self.buff_type = skill.buff_type
        self.buff_value = skill.buff_value
        self.learn_lv = skill.learn_lv
