from typing import List
from .models import Users, ActiveSkillConfig, UserSkillInfo, WeaponConfig, PassiveSkill, check_column    # noqa: F401
from ..version import __version__
from .config import add_config
from nonebot import get_driver


class DB:

    @classmethod
    def init(cls) -> None:
        from .basemodel import Base, engine
        Base.metadata.create_all(engine)
        check_column()
        add_config()

    # -----------------User_start----------------#
    @classmethod
    def get_user_by_user_id(cls, user_id):
        return Users.query([Users], filter=[Users.user_id == int(user_id)], query_first=True)

    @classmethod
    def update_user(cls, user):
        return Users.update(user.to_dict(), [Users.id == user.id])

    # -----------------Skill_info_start----------------#
    @classmethod
    def get_skill_by_name(cls, skill_name):
        # 根据技能名称获取技能信息
        return ActiveSkillConfig.query([ActiveSkillConfig], filter=[ActiveSkillConfig.name == skill_name, ActiveSkillConfig.version == __version__], query_first=True)

    # -----------------User_skill_start----------------#
    @classmethod
    def get_user_skill_list(cls, user, skill_type=None) -> List:
        '''获取用户拥有的所有技能
        pram:user对象
        pram:skill_type:被动-passive;主动-active
        '''
        if skill_type:
            result = UserSkillInfo.query([UserSkillInfo.skill_id, UserSkillInfo.skill_level, ActiveSkillConfig.skill_type],
                                           filter=[UserSkillInfo.user_id == user.user_id, ActiveSkillConfig.skill_type ==
                                                   skill_type, ActiveSkillConfig.version == __version__],
                                           join=[
                                               ActiveSkillConfig, UserSkillInfo.skill_id == ActiveSkillConfig.id]
                                           )
        else:
            result = UserSkillInfo.query([UserSkillInfo.skill_id, UserSkillInfo.skill_level, ActiveSkillConfig.skill_type],
                                           filter=[
                                               UserSkillInfo.user_id == user.user_id, ActiveSkillConfig.version == __version__],
                                           join=[
                                               ActiveSkillConfig, UserSkillInfo.skill_id == ActiveSkillConfig.id]
                                           )
        return result

    @classmethod
    def get_user_skill_info(cls, user, skill_id):
        '''获取用户单个技能信息'''
        return UserSkillInfo.query([UserSkillInfo], filter=[UserSkillInfo.user_id == user.user_id, UserSkillInfo.skill_id == skill_id], query_first=True)

    @classmethod
    def get_user_ps_skills_info(cls, user):
        '''获取用户所有被动技能信息'''
        return UserSkillInfo.query([UserSkillInfo.skill_group_id, PassiveSkill.buff_type, PassiveSkill.buff_value],
                                   filter=[UserSkillInfo.user_id == user.user_id, UserSkillInfo.skill_type == '被动'],
                                   join=[PassiveSkill, UserSkillInfo.skill_id == PassiveSkill.id]
                                   )

    @classmethod
    def get_active_skill_by_id(cls, active_skill_id):
        '''获取单个主动技能的信息'''
        return ActiveSkillConfig.query([ActiveSkillConfig], filter=[ActiveSkillConfig.id == active_skill_id, ActiveSkillConfig.version == __version__], query_first=True)

    @classmethod
    def get_passive_skill_by_id(cls, passive_skill_id):
        '''获取单个被动技能的信息'''
        return PassiveSkill.query([PassiveSkill], filter=[PassiveSkill.id == passive_skill_id, PassiveSkill.version == __version__], query_first=True)

    @classmethod
    def get_weapon_by_id(cls, weapon_id):
        '''获取单个武器信息'''
        return WeaponConfig.query([WeaponConfig], filter=[WeaponConfig.id == weapon_id, WeaponConfig.version == __version__], query_first=True)


get_driver().on_startup(DB.init)
