from .util import get_probability


class Weapon:
    def __init__(self, weapon) -> None:
        if weapon == 0:
            self.weapon_id = 0
            self.miss = 0
            self.min_atk = 0
            self.max_atk = 0
            self.type = 0
            self.weapon_name = 0
            # 反击
            self.after_fanji = False
            self.after_fanji_probability = 0
            self.before_fanji = False
            self.before_fanji_probability = 0
            # 连击
            self.double_hit = False
            self.double_hit_probability = 0
            self.double_hit_count = 0
            # 必中
            self.bizhong = False
            # 忽略假死
            self.ignore_jiasi = False
            # 命中率
            self.hitting_accuracy = 5
            # 是否可以反击
            self.can_fanji = False
            # 反击闪避率
            self.fanji_miss = 0
            # ---忽略回合
            self.is_turn_pass = False
            self.is_turn_pass_probability = 100
            self.pass_turn = 1
            # --吸血
            self.absorb = 0
            # 忽视大海无量
            self.miss_dhwl = False
            # 反击miss率
            self.fanji_miss = 0
            # 同性增伤
            self.same_sex_zs = 0
            # ---临时buff
            self.buff_type = ''
            self.buff_turn = 0
            self.buff_value = 0
            self.buff_zj = 'buff'
            self.buff_target = 'self'
            # ---额外伤害参数
            self.attribute_damage_type = False
            self.attribute_type = ''
            self.attribute_coefficient = 0
            # ----自己休息一回合
            self.rest = False
            self.rest_probability = 100
            # ----秒杀
            self.seckill = False
            self.seckill_probability = 100
            # ----低血量增伤
            self.low_hp_zs = False
            self.low_hp = 0
            self.low_hp_zs_value = 0
        else:
            self.weapon_id = weapon.id
            self.miss = weapon.miss
            self.min_atk = weapon.min_atk
            self.max_atk = weapon.max_atk
            self.weapon_type = weapon.weapon_type
            self.weapon_name = weapon.weapon_name
            # 反击
            self.after_fanji = weapon.after_fanji
            self.after_fanji_probability = weapon.after_fanji_probability
            self.before_fanji = weapon.before_fanji
            self.before_fanji_probability = weapon.before_fanji_probability
            # 连击
            self.double_hit = weapon.double_hit
            self.double_hit_probability = weapon.double_hit_probability
            self.double_hit_count = weapon.double_hit_count
            # 必中
            self.bizhong = weapon.bizhong
            # 忽略假死
            self.ignore_jiasi = weapon.ignore_jiasi
            # 命中率
            self.hitting_accuracy = weapon.hitting_accuracy
            # 是否可以反击
            self.can_fanji = weapon.can_fanji
            # 反击闪避率
            self.fanji_miss = weapon.fanji_miss
            # ---忽略回合
            self.is_turn_pass = weapon.is_turn_pass
            self.is_turn_pass_probability = weapon.is_turn_pass_probability
            self.pass_turn = weapon.pass_turn
            # --吸血
            self.absorb = weapon.absorb
            # 忽视大海无量
            self.miss_dhwl = weapon.miss_dhwl
            # 反击miss率
            self.fanji_miss = weapon.fanji_miss
            # 同性增伤
            self.same_sex_zs = weapon.same_sex_zs
            # ---临时buff
            self.buff_type = weapon.buff_type
            self.buff_turn = weapon.buff_turn
            self.buff_value = weapon.buff_value
            self.buff_zj = weapon.buff_zj
            self.buff_target = weapon.buff_target
            # ---额外伤害参数
            self.attribute_damage_type = weapon.attribute_damage_type
            self.attribute_type = weapon.attribute_type
            self.attribute_coefficient = weapon.attribute_coefficient
            # ----自己休息一回合
            self.rest = weapon.rest
            self.rest_probability = weapon.rest_probability
            # ----秒杀
            self.seckill = weapon.seckill
            self.seckill_probability = weapon.seckill_probability
            # ----低血量增伤
            self.low_hp_zs = weapon.low_hp_zs
            self.low_hp = weapon.low_hp
            self.low_hp_zs_value = weapon.low_hp_zs_value

    def get_hit_count(self):
        hit = 1
        if self.double_hit and get_probability(self.double_hit_probability):
            hit = self.double_hit_count
        return hit

    def get_weapon_msg(self):
        msg = f'{self.weapon_name}:{self.weapon_type}武器,伤害:{self.min_atk}~{self.max_atk},'
        if self.attribute_damage_type:
            msg += f'附带{self.attribute_type}的{self.attribute_coefficient}%伤害,'
        if self.miss:
            msg += f'增加{self.miss}闪避率,'
        if self.hitting_accuracy:
            msg += f'增加{self.hitting_accuracy}命中率,'
        if self.after_fanji:
            msg += f'{self.after_fanji_probability}%的概率被攻击后反击,'
        if self.before_fanji:
            msg += f'{self.before_fanji_probability}%的概率被攻击前反击,'
        if self.double_hit:
            msg += f'{self.double_hit_probability}%的概率连续攻击{self.double_hit_count}次,'
        if self.bizhong:
            msg += '必中,'
        if self.ignore_jiasi:
            msg += '忽略假死,'
        if not self.can_fanji:
            msg += '不可反击,'
        if self.fanji_miss:
            msg += f'{self.fanji_miss}%的概率闪避反击,'
        if self.same_sex_zs:
            msg += f"对同性增伤{self.same_sex_zs}%,"
        if self.buff_type:
            if self.buff_zj == 'buff':
                if self.buff_target == 'self':
                    msg += f'增加自身{self.buff_type}{self.buff_value}点持续{self.buff_turn}回合,'
                elif self.buff_target == 'target':
                    msg += f'增加对方{self.buff_type}{self.buff_value}点持续{self.buff_turn}回合,'
            elif self.buff_zj == 'debuff':
                if self.buff_target == 'self':
                    msg += f'减少自身{self.buff_type}{self.buff_value}点持续{self.buff_turn}回合,'
                elif self.buff_target == 'target':
                    msg += f'减少对方{self.buff_type}{self.buff_value}点持续{self.buff_turn}回合,'
        if self.is_turn_pass:
            msg += f'{self.is_turn_pass_probability}%的概率忽略对手{self.pass_turn}个回合,'
        if self.rest:
            msg += f'自身{self.rest_probability}%的概率休息一回合,'
        if self.seckill:
            msg += f'有{self.seckill_probability}的概率秒杀对手,'
        if self.low_hp_zs:
            msg += f'血量低于{self.low_hp}%的时候伤害增加{self.low_hp_zs_value}%,'
        return msg[:-1]
