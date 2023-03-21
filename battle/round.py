from .weapon import Weapon
from .active_skill import ActiveSkill
import random
from .player import TempAttribute
from ..database.db import DB
from .util import (
    MISSMSG,
    BEFOREATTACKMSG,
    AFTERATTACKMSG,
    WEAPONHITMSG,
    HITMSG,
    WEAPONBIZHONGMSG,
    JIASIMSG,
    DOTMSG,
    IGNOREJIASI,
    SKILLBIZHONGMSG,
    SKILLMSG,
    REMOVEHPMSG,
    REMOVEHPMISSMSG,
    DOTDAMAGEMSG,
    SKILLTURNPASSMSG,
    WEAPONTURNPASSMSG,
    RECOVERHPMSG,
    RESETDOTMSG,
    NOTHROWWEAPONSMSG,
    THROWWEAPONSMSG,
    CANTFANJIMSG,
    LIMITSKILLMISSMSG,
    LIMITSKILLMSG,
    LIMITACTIVEMSG,
    TARGETTHROWWEAPONMSG,
    BUFFMSG,
    SPEEDEFFECTMSG,
    FANJIMISSMSG,
    ABSORBMSG,
    DHWLMSG,
    RESTMSG,
    SECKILLMSG,
    get_probability
)


class Round:
    def __init__(self, count, p1, p2, battle_msg) -> None:
        self.count = count
        self.p1 = p1
        self.p2 = p2
        self.battle_msg = battle_msg

    def get_next_round(self):
        self.turn_action()
        self.get_speed_effect_turn_pass(self.p1, self.p2)
        self.reset_player_skill_and_weapon()
        self.battle_msg.append(
            f'{self.p1.nick_name}当前血量：{self.p1.hp}，{self.p2.nick_name}当前血量：{self.p2.hp}')
        if self.p1.is_alive():
            pass
        else:
            if self.p1.is_jiasi:
                self.p1.hp = 1
                self.p1.is_jiasi = False
                self.battle_msg.append(JIASIMSG.format(self.p1.nick_name))
            else:
                self.battle_msg.append(f'{self.p2.nick_name}胜利了')
        if self.p2.is_alive():
            is_turn_pass, self.p2 = self.get_turn_pass(self.p2)
            if not is_turn_pass:
                self.p1, self.p2 = self.p2, self.p1
        else:
            if self.p2.is_jiasi:
                self.p2.hp = 1
                self.p2.is_jiasi = False
                self.battle_msg.append(JIASIMSG.format(self.p2.nick_name))
                is_turn_pass, self.p2 = self.get_turn_pass(self.p2)
                if not is_turn_pass:
                    self.p1, self.p2 = self.p2, self.p1
                return self.p1, self.p2, self.battle_msg
            else:
                self.battle_msg.append(f'{self.p1.nick_name}胜利了')
        return self.p1, self.p2, self.battle_msg

    def turn_action(self):
        self.battle_msg.append(self.turn_msg())
        if self.p1.dot_turn:
            self.p1.hp -= self.p1.dot_damage
            self.p1.dot_turn -= 1
            self.battle_msg.append(DOTMSG.format(
                self.p1.nick_name, self.p1.dot_name, self.p1.dot_damage, self.p1.dot_turn))

        if self.p2.dot_turn:
            self.p2.hp -= self.p2.dot_damage
            self.p2.dot_turn -= 1
            self.battle_msg.append(DOTMSG.format(
                self.p2.nick_name, self.p2.dot_name, self.p2.dot_damage, self.p2.dot_turn))
        if not self.p1.is_alive():
            return
        if not self.p2.is_alive():
            return

        p1_attack_type = self.p1.get_attack_type()
        if self.p1.is_miss(target=self.p2):
            # miss了，判断必中
            if self.p1.get_bizhong():
                # 必中逻辑
                if p1_attack_type == 1:
                    self.battle_msg.append(SKILLBIZHONGMSG.format(
                        self.p2.nick_name,
                        self.p1.nick_name,
                        self.p1.nick_name,
                        self.p1.now_active_skill.skill_name))

                elif p1_attack_type == 2:
                    self.battle_msg.append(WEAPONBIZHONGMSG.format(
                        self.p2.nick_name,
                        self.p1.nick_name,
                        self.p1.nick_name,
                        self.p1.now_weapon.weapon_name))
                self.p1, self.p2 = self.attack(
                    self.p1, self.p2, atk_type=p1_attack_type)
            else:
                # 没必中 miss了
                self.battle_msg.append(MISSMSG.format(
                    self.p1.nick_name, self.p2.nick_name))
                return
        else:
            # 没miss
            if self.p2.is_before_fanji():  # p2反击
                if not self.get_can_fanji_msg():
                    pass
                else:  # 可以反击
                    self.battle_msg.append(BEFOREATTACKMSG.format(
                        self.p1.nick_name, self.p2.nick_name))
                    self.p1, self.p2 = self.get_before_fanji_msg(
                        p1=self.p1, p2=self.p2)
                    if not self.p1.is_alive():
                        return
            self.p1, self.p2 = self.attack(
                self.p1, self.p2, atk_type=p1_attack_type)
        # 被打了，判断反击
        if not self.get_can_fanji_msg():
            pass
        else:
            self.p1, self.p2 = self.get_after_fanji_msg(p1=self.p1, p2=self.p2)

    def get_can_fanji_msg(self):
        if not self.p1.get_can_fanji():  # p1无法被反击
            self.battle_msg.append(CANTFANJIMSG.format(
                self.p2.nick_name, self.p1.nick_name))
            return False
        if not self.p1.get_fanji_miss():  # 反击miss
            self.battle_msg.append(FANJIMISSMSG.format(
                self.p2.nick_name, self.p1.nick_name))
            return False
        return True

    def get_before_fanji_msg(self, p1, p2):
        p2_attack_type = p2.get_attack_type()
        p2, p1 = self.attack(p2, p1, atk_type=p2_attack_type)
        return p1, p2

    def get_after_fanji_msg(self, p1, p2):
        if p2.is_alive():
            if p2.is_after_fanji():
                self.battle_msg.append(
                    AFTERATTACKMSG.format(p2.nick_name))
                p2_attack_type = p2.get_attack_type()
                p2, p1 = self.attack(self.p2, self.p1, atk_type=p2_attack_type)
        return p1, p2

    def turn_msg(self) -> str:
        return f'当前为{self.p1.nick_name}的回合，回合数：{self.count}'

    def attack(self, p1, p2, atk_type):
        '''扣血方法'''
        if p1.limit_name != '':
            if p1.get_now_attack_far_and_near() == p1.limit_type:
                p1.limit_turn -= 1
                if p1.limit_turn == 0:
                    p1.limit_type = ''
                    p1.limit_name = ''
                pass
            else:
                self.battle_msg.append(LIMITACTIVEMSG.format(
                    p1.nick_name,
                    p1.get_now_attack_far_and_near(),
                    p1.limit_name
                ))
                p1.limit_turn -= 1
                if p1.limit_turn == 0:
                    p1.limit_type = ''
                    p1.limit_name = ''
                return p1, p2
        if atk_type == 0:
            atk = p1.power
            damage = int(atk * ((100 - p2.base_jianshang) / 100)
                         * (p1.base_zengshang / 100 + 1))
            self.battle_msg.append(HITMSG.format(
                p1.nick_name,
                p2.nick_name,
                damage
            ))
            p2.hp -= damage
            p1, p2 = self.get_dhwl_msg(p1, p2, damage)
            if not p1.is_alive():
                return p1, p2

        elif atk_type == 1:  # 技能
            if p1.now_active_skill.skill_type == '直接伤害':
                damage = self.get_skill_final_damage(p1, p2)
                self.battle_msg.append(SKILLMSG.format(
                    p1.nick_name,
                    p1.now_active_skill.skill_name,
                    p2.nick_name,
                    damage
                ))
                p2.hp -= damage
                p1, p2 = self.get_dhwl_msg(p1, p2, damage)
                if not p1.is_alive():
                    return p1, p2

            elif p1.now_active_skill.skill_type == '持续伤害':
                damage = self.get_skill_final_damage(p1, p2)
                p2.dot_damage = damage
                p2.dot_turn = p1.now_active_skill.dot_turn
                p2.dot_name = p1.now_active_skill.skill_name
                self.battle_msg.append(DOTDAMAGEMSG.format(
                    p1.nick_name,
                    p1.now_active_skill.skill_name,
                    p2.nick_name,
                    damage,
                    p1.now_active_skill.dot_turn,
                ))
            elif p1.now_active_skill.skill_type == '生命移除':
                if get_probability(p1.now_active_skill.remove_hp_probability):  # 命中了
                    p2 = p1.now_active_skill.target_hp_remove(p2)
                    self.battle_msg.append(REMOVEHPMSG.format(
                        p2.nick_name,
                        p1.nick_name,
                        p1.now_active_skill.skill_name,
                        p2.hp
                    ))
                else:
                    self.battle_msg.append(REMOVEHPMISSMSG.format(
                        p1.nick_name,
                        p1.now_active_skill.skill_name,
                        p2.nick_name,
                    ))
            elif p1.now_active_skill.skill_type == '恢复类':
                recover_hp, p1 = self.get_recover_hp(p1)
                self.battle_msg.append(RECOVERHPMSG.format(
                    p1.nick_name,
                    p1.now_active_skill.skill_name,
                    recover_hp
                ))
                if p1.now_active_skill.is_atk:
                    atk = p1.power
                    damage = int(atk * ((100 - p2.base_jianshang) / 100)
                                 * (p1.Base_zengshang / 100 + 1))
                    self.battle_msg.append(HITMSG.format(
                        p1.nick_name,
                        p2.nick_name,
                        damage
                    ))
                    p2.hp -= damage
                    p1, p2 = self.get_dhwl_msg(p1, p2, damage)
                    if not p1.is_alive():
                        return p1, p2
            elif p1.now_active_skill.skill_type == '扔武器':
                have_weapons = len(p1.weapons)
                count = p1.now_active_skill.throw_weapons if have_weapons >= p1.now_active_skill.throw_weapons else have_weapons
                if count == 0:
                    self.battle_msg.append(NOTHROWWEAPONSMSG.format(
                        p1.nick_name,
                        p1.now_active_skill.skill_name
                    ))
                else:
                    self.battle_msg.append(THROWWEAPONSMSG.format(
                        p1.nick_name,
                        p1.now_active_skill.skill_name
                    ))
                    while count:
                        use = random.choice(p1.weapons)
                        p1.now_weapon = Weapon(DB.get_weapon_by_id(use))
                        p1.weapons.remove(use)
                        p1, p2 = self.weapon_action(p1, p2)
                        count -= 1
                    p1.now_weapon = Weapon(0)  # 重置
            elif p1.now_active_skill.skill_type == '限制':
                if get_probability(p1.now_active_skill.limit_base_probability):
                    p2.limit_type = p1.now_active_skill.limit_type
                    p2.limit_turn = p1.now_active_skill.limit_turn
                    p2.limit_name = p1.now_active_skill.skill_name
                    self.battle_msg.append(LIMITSKILLMSG.format(
                        p1.nick_name,
                        p1.now_active_skill.skill_name,
                        p2.nick_name,
                        p2.nick_name,
                        p2.limit_type
                    ))
                else:
                    self.battle_msg.append(LIMITSKILLMISSMSG.format(
                        p1.nick_name,
                        p1.now_active_skill.skill_name,
                        p2.nick_name,
                    ))

            if not p2.is_alive():  # 打死了
                if p1.now_active_skill.ignore_jiasi and p2.is_jiasi:  # 假死碰上忽略假死
                    p2.is_jiasi = False
                    self.battle_msg.append(
                        IGNOREJIASI.format(p2.nick_name, p1.nick_name))
                    return p1, p2

            if p1.now_active_skill.is_target_throw_weapons:
                skill_throw_weapon_count = p1.now_active_skill.is_target_throw_weapons
                p2_weapons_count = len(p2.weapons)
                count = p2_weapons_count if skill_throw_weapon_count >= p2_weapons_count else skill_throw_weapon_count
                THROWWEAPONMSG = TARGETTHROWWEAPONMSG.format(
                    p1.nick_name, p1.now_active_skill.skill_name, p2.nick_name)
                if count > 0:
                    while count:
                        throw = random.choice(p2.weapons)
                        p2.weapons.remove(throw)
                        weapon_info = Weapon(DB.get_weapon_by_id(throw))
                        THROWWEAPONMSG += f'{weapon_info.weapon_name}、'
                        count -= 1
                    THROWWEAPONMSG = THROWWEAPONMSG[:-1] + '被丢弃了！'
                    self.battle_msg.append(THROWWEAPONMSG)
            if p1.now_active_skill.buff_type:
                count = len(p1.temp_attribute) + 1
                count = str(count)
                count = TempAttribute(p1.now_active_skill)
                p1.temp_attribute.append(count)
                self.battle_msg.append(BUFFMSG.format(
                    p1.nick_name,
                    '技能',
                    p1.now_active_skill.skill_name,
                    p1.nick_name,
                    p1.now_active_skill.buff_type,
                    p1.now_active_skill.buff_value,
                    p1.now_active_skill.buff_turn,
                ))

            if p1.now_active_skill.is_turn_pass:  # 忽略回合
                if get_probability(p1.now_active_skill.is_turn_pass_probability):
                    self.battle_msg.append(SKILLTURNPASSMSG.format(
                        p1.nick_name,
                        p1.now_active_skill.skill_name,
                        p2.nick_name,
                        p2.nick_name,
                        p1.now_active_skill.pass_turn
                    ))
                    p2.is_turn_pass = True
                    p2.pass_turn = p1.now_active_skill.pass_turn

        elif atk_type == 2:  # 武器
            p1, p2 = self.weapon_action(p1, p2)
            if not p2.is_alive():  # 打死了
                if p1.now_weapon.ignore_jiasi and p2.is_jiasi:  # 假死碰上忽略假死
                    p2.is_jiasi = False
                    self.battle_msg.append(
                        IGNOREJIASI.format(p2.nick_name, p1.nick_name))
                    return p1, p2
            if p1.now_weapon.is_turn_pass:  # 忽略回合
                if get_probability(p1.now_weapon.is_turn_pass_probability):
                    self.battle_msg.append(WEAPONTURNPASSMSG.format(
                        p1.nick_name,
                        p1.now_active_skill.skill_name,
                        p2.nick_name,
                        p2.nick_name,
                        p1.now_active_skill.pass_turn
                    ))
                    p2.is_turn_pass = True
                    p2.pass_turn = p1.now_weapon.pass_turn
            if p1.now_weapon.buff_type:
                if p1.now_weapon.buff_target == 'self':
                    self.battle_msg.append(BUFFMSG.format(
                        p1.nick_name,
                        '武器',
                        p1.now_weapon.weapon_name,
                        p1.nick_name,
                        p1.now_weapon.buff_type,
                        p1.now_weapon.buff_value,
                        p1.now_weapon.buff_turn,
                    ))
                    count = len(p1.temp_attribute) + 1
                    count = str(count)
                    count = TempAttribute(p1.now_weapon)
                    p1.temp_attribute.append(count)
                elif p1.now_weapon.buff_target == 'target':
                    self.battle_msg.append(BUFFMSG.format(
                        p1.nick_name,
                        '武器',
                        p1.now_weapon.weapon_name,
                        p2.nick_name,
                        p1.now_weapon.buff_type,
                        p1.now_weapon.buff_value,
                        p1.now_weapon.buff_turn,
                    ))
                    count = len(p2.temp_attribute) + 1
                    count = str(count)
                    count = TempAttribute(p1.now_weapon)
                    p2.temp_attribute.append(count)
            if p1.now_weapon.rest:
                if get_probability(p1.now_weapon.rest_probability):
                    self.battle_msg.append(RESTMSG.format(p1.nick_name))
                    p1.is_turn_pass = True
                    p1.pass_turn = 1
            if p1.now_weapon.seckill:
                if get_probability(p1.now_weapon.seckill_probability):
                    self.battle_msg.append(
                        SECKILLMSG.format(p1.nick_name, p2.nick_name))
                    p2.hp = -1
                    if p2.is_jiasi:
                        p2.is_jiasi = False
        return p1, p2

    def weapon_action(self, p1, p2):
        atk = p1.get_weapon_damage(p2)
        hit = p1.now_weapon.get_hit_count()
        if p1.now_weapon.weapon_type == '小型':
            damage = int(atk * ((100 - p2.small_weaponjs - p2.base_jianshang) / 100)
                         * ((p1.small_weaponzs / 100) + 1) * hit)

        elif p1.now_weapon.weapon_type == '中型':
            damage = int(atk * ((100 - p2.medium_weaponjs - p2.base_jianshang) / 100)
                         * ((p1.medium_weaponzs / 100) + 1) * hit)

        elif p1.now_weapon.weapon_type == '大型':
            damage = int(atk * ((100 - p2.large_weaponjs - p2.base_jianshang) / 100)
                         * ((p1.large_weaponzs / 100) + 1) * hit)

        self.battle_msg.append(WEAPONHITMSG.format(
            p1.nick_name,
            p1.now_weapon.weapon_name,
            p2.nick_name,
            hit,
            damage))
        if p1.get_absorb():
            absorb_hp = int(p1.get_absorb() * damage / 100)
            p1.hp += absorb_hp
            self.battle_msg.append(ABSORBMSG.format(
                p1.nick_name,
                '武器',
                p1.nick_name,
                absorb_hp))
        p2.hp -= damage
        p1, p2 = self.get_dhwl_msg(p1, p2, damage)
        return p1, p2

    def get_skill_final_damage(self, p1, p2):
        skill_base_damage = p1.now_active_skill.get_base_damage(p1)
        base_zs = p1.base_zengshang / 100 + 1
        p1_active_skill_zs = (p1.active_skill_zs / 100) + 1  # 主动技能增伤
        p2_active_skill_js = (100 - p2.active_skill_js) / 100  # 主动技能减伤
        opposite_sex_zengshang = 1
        crit = 1
        if get_probability(p1.active_skill_crit):
            crit = 1.5
        if p1.now_active_skill.opposite_sex_zengshang:  # 异性增伤
            if not p1.is_opposite_sex(p2):
                opposite_sex_zengshang = (
                    p1.now_active_skill.opposite_sex_zengshang / 100) + 1
        return int(skill_base_damage * p1_active_skill_zs * p2_active_skill_js * opposite_sex_zengshang * base_zs * crit)

    def get_turn_pass(self, target):
        if target.is_turn_pass:
            if target.pass_turn:  # 非0
                target.pass_turn -= 1
                return True, target
            else:  # 0
                target.is_turn_pass = False
                return False, target
        else:
            return False, target

    def get_recover_hp(self, p1):
        hp = int(p1.hp * p1.now_active_skill.recover_hp / 100)
        if p1.hp + hp > p1.all_hp:
            hp = p1.all_hp - p1.hp
        p1.hp += hp
        if p1.now_active_skill.reset_dot:
            if p1.dot_turn:
                p1.dot_damage = 0
                p1.dot_turn = 0
                p1.dot_name = ''
                self.battle_msg(RESETDOTMSG.format(
                    p1.now_active_skill.skill_name, p1.nick_name))
        return hp, p1

    def reset_player_skill_and_weapon(self):
        self.p1.now_weapon = Weapon(0)
        self.p1.now_active_skill = ActiveSkill(0)
        self.p2.now_weapon = Weapon(0)
        self.p2.now_active_skill = ActiveSkill(0)
        self.p1.get_buff()
        self.p2.get_buff()

    def get_speed_effect_turn_pass(self, p1, p2):
        turn_pass = p1.get_speed_effect(p2)
        if turn_pass:
            self.battle_msg.append(SPEEDEFFECTMSG.format(
                p1.nick_name,
                p2.nick_name,
                p2.nick_name,
            ))
            p2.is_turn_pass = True
            p2.pass_turn = 1
        return p1, p2

    def get_dhwl_msg(self, p1, p2, damage):
        if p2.dhwl and (p1.now_weapon.miss_dhwl or p1.now_active_skill.miss_dhwl):
            hp = int(damage * p2.dhwl_value / 100)
            p1.hp -= hp
            self.battle_msg.append(DHWLMSG.format(
                p1.nick_name,
                p2.nick_name,
                hp
            ))
            return p1, p2
        else:
            return p1, p2
