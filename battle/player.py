import random
import numpy as np
from .weapon import Weapon
from .active_skill import ActiveSkill
from .util import get_probability
from .character import Character
from ..database.db import DB


class Player(Character):

    def __init__(self, player) -> None:
        super().__init__(player)
        self.all_hp = self.hp  # 用于战斗计算
        self.now_weapon = Weapon(0)
        self.active_skills = [1, 7, 13, 19, 25,
                              31, 37, 43, 49, 55, 61, 67, 73, 78]
        self.weapons = [1, 7, 13, 19, 25, 31, 37, 43, 49, 55, 61, 67, 73, 78]
        self.now_active_skill = ActiveSkill(0)
        # -------dot-------
        self.dot_damage = 0
        self.dot_turn = 0
        self.dot_name = ''
        # -------buff-------
        self.temp_attribute = []
        # -------限制-------
        self.limit_type = ''
        self.limit_turn = 0
        self.limit_name = ''
        # -------忽略回合----
        self.is_turn_pass = False
        self.pass_turn = 0

    def is_alive(self):
        '''判断用户是否存活'''
        return self.hp > 0

    def is_opposite_sex(self, target):
        '''判断与目标是否同性'''
        return self.gender == target.gender

    def get_can_fanji(self):
        return self.now_active_skill.can_fanji or self.now_weapon.can_fanji

    def is_before_fanji(self):
        weapon_before_fanji_probability = 0
        if self.now_weapon.before_fanji:
            weapon_before_fanji_probability = self.now_weapon.before_fanji_probability
        return get_probability(self.before_fanji_probability + weapon_before_fanji_probability)

    def is_after_fanji(self):
        weapon_after_fanji_probability = 0
        if self.now_weapon.after_fanji:
            weapon_after_fanji_probability = self.now_weapon.after_fanji_probability
        return get_probability(self.after_fanji_probability + weapon_after_fanji_probability)

    def is_miss(self, target):   # 是否miss
        dif = target.agility - self.agility
        if dif <= 0:
            probability = 0
        else:
            probability = 5 * np.log(dif + 10)   # 敏捷差提供的miss率
            '''
            曲线
            import matplotlib.pyplot as plt
            import numpy as np
            x = np.arange(0, 100, 1)
            y = 5 * np.log(x + 10)
            plt.title("5 * log(x + 10)")
            plt.plot(x, y)
            plt.show()
            '''
        target_weapon_miss = target.now_weapon.miss  # target武器提供的miss率
        self_now_weapon_hitting_accuracy = self.now_weapon.hitting_accuracy   # 自己武器的命中率
        self_now_skill_hitting_accuracy = self.now_active_skill.hitting_accuracy  # 自己技能的命中率
        other_miss = 0  # 对应武器种类的miss率
        if self.now_weapon.weapon_id != 0:
            if self.now_weapon.weapon_type == '小型':
                other_miss = target.small_miss - self.small_hitting_accuracy
            if self.now_weapon.weapon_type == '中型':
                other_miss = target.medium_miss - self.medium_hitting_accuracy
            if self.now_weapon.weapon_type == '大型':
                other_miss = target.large_miss - self.large_hitting_accuracy
        if self.now_active_skill != 0:
            other_miss = target.active_skill_miss - self.active_skill_hitting_accuracy
        return random.uniform(0, 100) < probability + target_weapon_miss + other_miss + target.base_miss - self_now_weapon_hitting_accuracy - self_now_skill_hitting_accuracy - self.base_hitting_accuracy

    def get_speed_effect(self, target):
        dif = self.speed - target.speed
        if dif <= 0:
            probability = 0
        else:
            probability = 10 * np.log(dif + 5)
        return random.uniform(0, 100) < probability + self.bass_speed_effect

    def get_attack_type(self):
        '''获取攻击类型
        attack_type 0-赤手空拳，1-技能，2-武器
        '''
        skill_probability = 40  # 技能概率
        weapon_probability = 40  # 武器概率
        probability = random.randint(0, 100)
        attack_type = 1 if probability <= skill_probability else 2 if probability <= weapon_probability + \
            skill_probability else 0
        if self.active_skills and attack_type == 1:
            use = random.choice(self.active_skills)
            self.now_active_skill = ActiveSkill(DB.get_active_skill_by_id(use))
            self.active_skills.remove(use)
        elif self.weapons and attack_type == 2:
            use = random.choice(self.weapons)
            self.now_weapon = Weapon(DB.get_weapon_by_id(use))
            self.weapons.remove(use)
        else:
            attack_type = 0
        return attack_type

    def get_bizhong(self):
        '''获取必中信息'''
        return self.now_active_skill.bizhong or self.now_weapon.bizhong

    def get_now_attack_far_and_near(self):
        if self.now_active_skill.skill_id != 0:
            return self.now_active_skill.far_and_near
        elif self.now_weapon.weapon_id != 0:
            return self.now_weapon.far_and_near
        else:
            return '近'  # 赤手空拳为近战

    def set_buff(self, buff):
        self.temp_attribute.append(buff)

    def get_buff(self):
        if self.temp_attribute != []:
            count = len(self.temp_attribute)
            while count:
                buff = self.temp_attribute[count - 1]
                self = buff.get_buff_type(self)
                count -= 1

    def get_absorb(self):
        return self.base_absorb + self.now_active_skill.absorb + self.now_weapon.absorb

    def get_fanji_miss(self):
        return get_probability(self.base_fanji_miss + self.now_active_skill.fanji_miss + self.now_weapon.can_fanji)

    def get_weapon_damage(self, target):
        '''获取当前武器的伤害'''
        base_zs = self.base_zengshang / 100 + 1
        same_sex_zs = 1
        if self.now_weapon.same_sex_zs and self.is_opposite_sex(target):
            same_sex_zs = (same_sex_zs + self.now_weapon.same_sex_zs) / 100
        attribute_damage = 0
        if self.now_weapon.attribute_damage_type:
            if self.now_weapon.attribute_type == '力量':
                attribute_damage = self.now_weapon.attribute_coefficient * self.power / 100
            if self.now_weapon.attribute_type == '敏捷':
                attribute_damage = self.now_weapon.attribute_coefficient * self.agility / 100
            if self.now_weapon.attribute_type == '速度':
                attribute_damage = self.now_weapon.attribute_coefficient * self.speed / 100
        low_hp_zs = 1
        if self.now_weapon.low_hp:
            if (self.hp / self.all_hp) <= (self.now_weapon.low_hp / 100):
                low_hp_zs = (100 + self.now_weapon.low_hp_zs_value) / 100
        return (self.power + random.randint(self.now_weapon.min_atk, self.now_weapon.max_atk) + attribute_damage) * same_sex_zs * low_hp_zs * base_zs


class TempAttribute:
    def __init__(self, buff) -> None:
        try:
            self.temp_name = buff.skill_name
        except Exception:
            self.temp_name = buff.weapon_name
        self.temp_type = buff.buff_type
        self.temp_turn = buff.buff_turn
        self.temp_value = buff.buff_value
        self.temp_zj = buff.buff_zj
        self.temp_flag = False

    def get_buff_type(self, player):
        if self.temp_flag:
            # 已经生效
            if self.temp_turn == 0:
                player = self.remove_player_temp_attribute(player)
                player.temp_attribute.remove(self)
                return player
            else:
                self.temp_turn -= 1
                return player
        else:
            # 未生效
            player = self.set_player_temp_attribute(player)
            self.temp_flag = True
            self.temp_turn -= 1
            return player

    def set_player_temp_attribute(self, player):
        if self.temp_zj == 'buff':
            if self.temp_type == '力量':
                player.power += self.temp_value
            if self.temp_type == '敏捷':
                player.power += self.temp_value
            if self.temp_type == '速度':
                player.speed += self.temp_value
            if self.temp_type == '闪避':
                player.base_miss += self.temp_value
            if self.temp_type == '命中':
                player.base_hitting_accuracy += self.temp_value

        elif self.temp_zj == 'debuff':
            if self.temp_type == '力量':
                player.power -= self.temp_value
            if self.temp_type == '敏捷':
                player.power -= self.temp_value
            if self.temp_type == '速度':
                player.speed -= self.temp_value
            if self.temp_type == '闪避':
                player.base_miss -= self.temp_value
            if self.temp_type == '命中':
                player.base_hitting_accuracy -= self.temp_value

        return player

    def remove_player_temp_attribute(self, player):
        if self.temp_zj == 'buff':
            if self.temp_type == '力量':
                player.power -= self.temp_value
            if self.temp_type == '敏捷':
                player.power -= self.temp_value
            if self.temp_type == '速度':
                player.speed -= self.temp_value
            if self.temp_type == '闪避':
                player.base_miss -= self.temp_value
            if self.temp_type == '命中':
                player.base_hitting_accuracy -= self.temp_value
        elif self.temp_zj == 'debuff':
            if self.temp_type == '力量':
                player.power += self.temp_value
            if self.temp_type == '敏捷':
                player.power += self.temp_value
            if self.temp_type == '速度':
                player.speed += self.temp_value
            if self.temp_type == '闪避':
                player.base_miss += self.temp_value
            if self.temp_type == '命中':
                player.base_hitting_accuracy += self.temp_value

        return player
