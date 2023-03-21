from .basemodel import Base, BaseModel, engine
from sqlalchemy import Integer, String, Column, DATETIME, Enum, BOOLEAN, text, inspect
import datetime
from sqlalchemy.orm.attributes import InstrumentedAttribute


class Users(Base, BaseModel):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, comment="用户QQ号")
    group_id = Column(Integer, comment="用户群号")
    nick_name = Column(String(10), comment="用户昵称")
    exp = Column(Integer, default=0, comment="经验")
    level = Column(Integer, default=1, comment="等级")
    gender = Column(Enum("male", "female"), default="male", comment="性别")
    physical_strength = Column(Integer, default=100, comment="用户体力")
    vigour = Column(Integer, default=50, comment="用户活力")
    base_hp = Column(Integer, default=62, comment="用户基础血量")
    level_up_hp = Column(Integer, default=0, comment="用户升级获得的血量")
    power = Column(Integer, comment="力量")
    agility = Column(Integer, comment="敏捷")
    speed = Column(Integer, comment="速度")
    update_time = Column(
        DATETIME, default=datetime.datetime.now, comment="更新时间")
    create_time = Column(
        DATETIME, default=datetime.datetime.now, comment="创建时间")


class Userleveltitleconfig(Base, BaseModel):
    __tablename__ = "Userleveltitleconfig"
    level = Column(Integer, primary_key=True, comment="等级")
    title = Column(String(10), comment="称号")
    version = Column(String(10), comment="版本")


class PassiveSkill(Base, BaseModel):
    __tablename__ = "PassiveSkill"
    id = Column(Integer, primary_key=True, comment="技能编号")
    group_id = Column(Integer, comment="技能组id")
    ps_name = Column(String(10), comment="技能名称")
    ps_lv = Column(Integer, comment="技能等级")
    buff_type = Column(String(10), comment="增幅类型")
    buff_value = Column(Integer, default=0, comment="增幅数值")
    learn_lv = Column(Integer, comment="学习等级")
    version = Column(String(10), comment="版本")


class ActiveSkillConfig(Base, BaseModel):
    __tablename__ = "ActiveSkillConfig"
    id = Column(Integer, primary_key=True, comment="技能编号")
    skill_name = Column(String(10), comment="技能名称")
    skill_level = Column(Integer, comment="技能等级")
    skill_type = Column(String(10), comment="技能类型")
    group_id = Column(Integer, comment="技能的种类id")
    base_damage = Column(Integer, default=0, comment="技能基础伤害")
    lv_damage_type = Column(BOOLEAN, default=False, comment="技能是否与人物等级挂钩")
    lv_coefficient = Column(Integer, default=0, comment="技能人物等级参数")
    attribute_damage_type = Column(
        BOOLEAN, default=False, comment="技能是否与人物属性挂钩")
    attribute_type = Column(String(10), default='', comment="技能人物属性类型")
    attribute_coefficient = Column(Integer, default=0, comment="技能人物属性参数")
    opposite_sex_zengshang = Column(Integer, default=0, comment="技能异性增伤参数")
    bizhong = Column(BOOLEAN, default=False, comment="技能是否必中")
    ignore_jiasi = Column(BOOLEAN, default=False, comment="技能是否忽略假死")
    hitting_accuracy = Column(Integer, default=0, comment="技能提供的命中")
    can_fanji = Column(BOOLEAN, default=True, comment="技能是否允许反击")
    far_and_near = Column(String(10), default='远', comment="技能的远近类型")
    miss_dhwl = Column(BOOLEAN, default=False, comment="技能是否忽视大海无量击")
    fanji_miss = Column(Integer, default=0, comment="闪避反击的概率")
    # ---生命移除类
    remove_hp_probability = Column(Integer, default=0, comment="生命移除概率百分比")
    remove_hp_surplus = Column(Integer, default=0, comment="生命移除至多少血")
    remove_hp_percentage = Column(Integer, default=0, comment="生命移除多少百分比血量")
    mix_remove_hp = Column(Integer, default=0, comment="生命移除最低剩余血量")
    # ---限制类
    limit_type = Column(String(10), default='', comment="技能限制类型")
    limit_base_probability = Column(Integer, default=0, comment="限制概率百分比")
    limit_turn = Column(Integer, default=0, comment="限制回合数")
    # ---dot持续回合
    dot_turn = Column(Integer, default=0, comment="持续回合")
    # ---忽略回合
    is_turn_pass = Column(BOOLEAN, default=False, comment="技能是否忽略对手回合")
    is_turn_pass_probability = Column(Integer, default=0, comment="忽略回合概率")
    pass_turn = Column(Integer, default=0, comment="忽略回合数")
    # ---恢复
    recover_hp = Column(Integer, default=0, comment="技能生命恢复百分比")
    is_atk = Column(BOOLEAN, default=True, comment="恢复后是否立马攻击")
    reset_dot = Column(BOOLEAN, default=False, comment="是否恢复自身dot")
    # ---扔武器参数
    throw_weapons = Column(Integer, default=0, comment="技能是否扔对面武器")
    # 丢对手武器
    is_target_throw_weapons = Column(Integer, default=0, comment="技能是否额外扔对面武器")
    # ---临时buff
    buff_type = Column(String(10), default='', comment="buff类型")
    buff_turn = Column(Integer, default=0, comment="buff持续回合")
    buff_value = Column(Integer, default=0, comment="buff的数值")
    buff_zj = Column(String(10), default='', comment="buff还是debuff")
    # ---技能吸血
    absorb = Column(Integer, default=0, comment="技能吸血")
    version = Column(String(10), comment="版本")


class UserSkillInfo(Base, BaseModel):
    __tablename__ = "UserSkillInfo"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_id = Column(Integer, comment="用户id")
    skill_id = Column(Integer, comment="技能id")
    skill_level = Column(Integer, comment="技能等级")
    skill_group_id = Column(Integer, comment="技能组id")
    skill_type = Column(String(10), comment="主动还是被动")
    update_time = Column(
        DATETIME, default=datetime.datetime.now, comment="更新时间")
    create_time = Column(
        DATETIME, default=datetime.datetime.now, comment="创建时间")


class WeaponConfig(Base, BaseModel):
    __tablename__ = "WeaponConfig"
    id = Column(Integer, primary_key=True, comment="编号")
    weapon_name = Column(String(10), comment="武器名称")
    min_atk = Column(Integer, comment="最小攻击")
    max_atk = Column(Integer, comment="最大攻击")
    weapon_type = Column(String(10), comment="武器类型")
    weapon_level = Column(Integer, default=0, comment="武器等级")
    miss = Column(Integer, default=0, comment="武器附带的miss率")
    after_fanji = Column(BOOLEAN, default=False, comment="被打后是否反击")
    after_fanji_probability = Column(Integer, default=0, comment="反击概率")
    before_fanji = Column(BOOLEAN, default=False, comment="被打前是否反击")
    before_fanji_probability = Column(Integer, default=0, comment="被打前反击概率")
    double_hit = Column(BOOLEAN, default=False, comment="是否连击")
    double_hit_probability = Column(Integer, default=0, comment="连击概率")
    double_hit_count = Column(Integer, default=0, comment="连击次数")
    bizhong = Column(BOOLEAN, default=False, comment="是否必中")
    absorb = Column(Integer, default=0, comment="吸血数值")
    miss_dhwl = Column(BOOLEAN, default=False, comment="是否无视大海无量")
    ignore_jiasi = Column(BOOLEAN, default=False, comment="是否忽略假死")
    is_turn_pass = Column(BOOLEAN, default=False, comment="是否忽略回合")
    is_turn_pass_probability = Column(Integer, default=0, comment="忽视回合的概率")
    pass_turn = Column(Integer, default=0, comment="忽视的回合")
    hitting_accuracy = Column(Integer, default=0, comment="命中率")
    can_fanji = Column(BOOLEAN, default=True, comment="是否可以反击")
    far_and_near = Column(String(10), comment="攻击的远近")
    fanji_miss = Column(Integer, default=0, comment="闪避反击的概率")
    same_sex_zs = Column(Integer, default=0, comment="同性增伤")
    buff_type = Column(String(10), default='', comment="buff类型")
    buff_turn = Column(Integer, default=0, comment="buff持续回合")
    buff_value = Column(Integer, default=0, comment="buff的值")
    buff_zj = Column(String(10), default='', comment="buff还是debuff")
    buff_target = Column(String(10), default='', comment="buff目标")
    attribute_damage_type = Column(BOOLEAN, default=False, comment="是否有属性增伤")
    attribute_type = Column(String(10), default='', comment="属性种类")
    attribute_coefficient = Column(Integer, default=0, comment="属性系数")
    rest = Column(BOOLEAN, default=False, comment="是否自己休息一回合")
    rest_probability = Column(Integer, default=0, comment="休息的概率")
    seckill = Column(BOOLEAN, default=False, comment="是否秒杀")
    seckill_probability = Column(Integer, default=0, comment="秒杀概率")
    low_hp_zs = Column(BOOLEAN, default=False, comment="低血量增伤")
    low_hp = Column(Integer, default=0, comment="血线")
    low_hp_zs_value = Column(Integer, default=0, comment="增伤数值")
    group_id = Column(Integer, comment="武器的种类id")
    group_type = Column(String(10), comment="武器的种类")
    version = Column(String(10), comment="版本")


def check_column():
    global_namespace = globals()
    insp = inspect(engine)
    db_tables = insp.get_table_names()
    for t in db_tables:
        db_table_column = [column['name']
                           for column in insp.get_columns(table_name=t)]
        class_obj = global_namespace.get(t)
        model_column = [attr for attr in dir(class_obj) if isinstance(
            getattr(class_obj, attr), InstrumentedAttribute)]
        not_in_table_column = []
        for column in model_column:
            if column not in db_table_column:
                not_in_table_column.append(column)
        if not_in_table_column != []:
            print(f"表{t}有新增列")
            with engine.connect() as con:
                for column in not_in_table_column:
                    sql = f"ALTER TABLE {t} ADD COLUMN {column}"
                    print(f'即将执行sql：{sql}')
                    con.execute(text(sql))
        else:
            print(f'没有新增列，表{t}检查完毕!')
