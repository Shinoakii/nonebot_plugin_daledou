class ActiveSkill:

    def __init__(self, skill) -> None:
        if skill == 0:
            self.skill_id = 0
            self.skill_name = ''
            self.skill_level = 0
            self.skill_type = ''
            # ---伤害类
            self.base_damage = 0
            self.lv_damage_type = False  # 等级伤害参数
            self.lv_coefficient = 0  # 等级系数
            self.attribute_damage_type = False
            self.attribute_type = ''
            self.attribute_coefficient = 0
            self.opposite_sex_zengshang = 0
            # ---生命移除类
            self.remove_hp_probability = 0
            self.remove_hp_surplus = 0  # 直接掉血
            self.remove_hp_percentage = 0  # 百分比扣血
            self.mix_remove_hp = 0
            # ---持续伤害属性
            self.dot_turn = 0
            # ---额外属性
            self.bizhong = False
            self.ignore_jiasi = False
            # ---限制类
            self.limit_type = ''
            self.limit_base_probability = 0
            self.limit_turn = 0
            # ---忽略回合
            self.is_turn_pass = False
            self.is_turn_pass_probability = 0
            self.pass_turn = 0
            # ---恢复
            self.recover_hp = 0
            self.is_atk = False
            self.reset_dot = False
            # ---扔武器参数
            self.throw_weapons = 0
            # 命中率
            self.hitting_accuracy = 0
            # 是否可以反击
            self.can_fanji = True
            self.far_and_near = '远'
            # 丢对手武器
            self.is_target_throw_weapons = 0
            # ---临时buff
            self.buff_type = ''
            self.buff_turn = 0
            self.buff_value = 0
            self.buff_zj = ''
            # ---技能吸血
            self.absorb = 0
            # 忽视大海无量
            self.miss_dhwl = False
            # 反击miss率
            self.fanji_miss = 0
        else:
            self.skill_id = skill.id
            self.skill_name = skill.skill_name
            self.skill_level = skill.skill_level
            self.skill_type = skill.skill_type
            # ---伤害类
            self.base_damage = skill.base_damage
            self.lv_damage_type = skill.lv_damage_type  # 等级伤害参数
            self.lv_coefficient = skill.lv_coefficient  # 等级系数
            self.attribute_damage_type = skill.attribute_damage_type
            self.attribute_type = skill.attribute_type
            self.attribute_coefficient = skill.attribute_coefficient
            self.opposite_sex_zengshang = skill.opposite_sex_zengshang
            # ---生命移除类
            self.remove_hp_probability = skill.remove_hp_probability
            self.remove_hp_surplus = skill.remove_hp_surplus  # 直接掉血
            self.remove_hp_percentage = skill.remove_hp_percentage  # 百分比扣血
            self.mix_remove_hp = skill.mix_remove_hp
            # ---持续伤害属性
            self.dot_turn = skill.dot_turn
            # ---额外属性
            self.bizhong = skill.bizhong
            self.ignore_jiasi = skill.ignore_jiasi
            # ---限制类
            self.limit_type = skill.limit_type
            self.limit_base_probability = skill.limit_base_probability
            self.limit_turn = skill.limit_turn
            # ---忽略回合
            self.is_turn_pass = skill.is_turn_pass
            self.is_turn_pass_probability = skill.is_turn_pass_probability
            self.pass_turn = skill.pass_turn
            # ---恢复
            self.recover_hp = skill.recover_hp
            self.is_atk = skill.is_atk
            self.reset_dot = skill.reset_dot
            # ---扔武器参数
            self.throw_weapons = skill.throw_weapons
            # 命中率
            self.hitting_accuracy = skill.hitting_accuracy
            # 是否可以反击
            self.can_fanji = skill.can_fanji
            self.far_and_near = skill.far_and_near
            # 丢对手武器
            self.is_target_throw_weapons = skill.is_target_throw_weapons
            # ---临时buff
            self.buff_type = skill.buff_type
            self.buff_turn = skill.buff_turn
            self.buff_value = skill.buff_value
            self.buff_zj = skill.buff_zj
            # ---技能吸血
            self.absorb = skill.absorb
            # 忽视大海无量
            self.miss_dhwl = skill.miss_dhwl
            # 反击miss率
            self.fanji_miss = skill.fanji_miss

    def get_skill_msg(self):
        msg = f'{self.skill_name}:{self.skill_type}技能,'
        if self.lv_damage_type:
            msg += f'伤害:{self.base_damage}+等级*{self.lv_coefficient}%,'
        elif self.attribute_damage_type:
            msg += f'伤害:{self.base_damage}+{self.attribute_type}*{self.attribute_coefficient}%,'
        else:
            if self.base_damage != 0:
                msg += f'基础伤害:{self.base_damage},'
        if self.dot_turn:
            msg += f'持续{self.dot_turn}回合,'
        if self.hitting_accuracy:
            msg += f'增加{self.hitting_accuracy}%命中率,'
        if self.bizhong:
            msg += '必中,'
        if self.ignore_jiasi:
            msg += '忽略假死,'
        if self.miss_dhwl:
            msg += '忽略大海无量,'
        if not self.can_fanji:
            msg += '不可反击,'
        if self.fanji_miss:
            msg += f'{self.fanji_miss}%的概率闪避反击,'
        if self.opposite_sex_zengshang:
            msg += f"对异性增伤{self.opposite_sex_zengshang}%,"
        if self.absorb:
            msg += f'技能附带{self.absorb}%的吸血,'
        if self.buff_type:
            if self.buff_zj == 'buff':
                msg += f'增加自身{self.buff_type}{self.buff_value}点持续{self.buff_turn}回合,'
            elif self.buff_zj == 'debuff':
                msg += f'减少自身{self.buff_type}{self.buff_value}点持续{self.buff_turn}回合,'
        if self.is_target_throw_weapons:
            msg += f'额外丢弃对方{self.is_target_throw_weapons}把武器,'
        if self.remove_hp_probability:
            if self.remove_hp_surplus:
                msg += f'有{self.remove_hp_probability}%的概率使对方生命值降低至{self.remove_hp_surplus},'
            if self.remove_hp_percentage:
                msg += f'有{self.remove_hp_probability}%的概率使对方生命值降低{self.remove_hp_probability}%,最少降低{self.mix_remove_hp}点血量,'
        if self.limit_type:
            msg += f'{self.limit_base_probability}%的几率限制对手只能进行{self.limit_type}程攻击,持续{self.limit_turn}回合,'
        if self.is_turn_pass:
            msg += f'{self.is_turn_pass_probability}%的概率忽略对手{self.pass_turn}个回合,'
        if self.recover_hp:
            msg += f'恢复自身{self.recover_hp}%的血量,'
            if self.is_atk:
                msg += '并且立马攻击,'
        if self.reset_dot:
            msg += '清空自身持续性伤害,'
        if self.throw_weapons:
            msg += f'丢弃对手{self.throw_weapons}把武器,'
        return msg[:-1]

    def get_base_damage(self, player):
        if self.lv_damage_type:
            return int(self.base_damage + (self.lv_coefficient * player.level / 100))
        if self.attribute_damage_type:
            if self.attribute_type == '力量':
                return int(self.base_damage + (self.attribute_coefficient * player.power / 100))
            if self.attribute_type == '敏捷':
                return int(self.base_damage + (self.attribute_coefficient * player.agility / 100))
            if self.attribute_type == '速度':
                return int(self.base_damage + (self.attribute_coefficient * player.speed / 100))
        else:
            return self.base_damage

    def target_hp_remove(self, target):
        if self.remove_hp_surplus:
            target.hp = self.remove_hp_surplus
        if self.remove_hp_percentage:
            remove_hp = int(target.hp * self.remove_hp_percentage / 100)
            if remove_hp > self.mix_remove_hp:
                target.hp -= remove_hp
            else:
                target.hp -= self.mix_remove_hp
        return target
