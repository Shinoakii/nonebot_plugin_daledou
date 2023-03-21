from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    GroupMessageEvent
)
from nonebot import on_command
from nonebot.params import CommandArg
from .database.db import DB
from .battle.weapon import Weapon
from .battle.active_skill import ActiveSkill
from .database.models import Users
import random
from .util import check_user


async def num_check(num):
    num = num.extract_plain_text().strip()
    if num:
        if not num.isdecimal():
            return False
        return num
    return False

qc_test_wq = on_command('Q武器')
qc_test_wq.handle()(check_user)


@qc_test_wq.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    num = await num_check(args)
    if num:
        result = DB.get_weapon_by_id(int(num))
        if result:
            weapon = Weapon(result)

            msg = weapon.get_weapon_msg()
            await qc_test_wq.finish(msg, at_sender=True)

        else:
            msg = '没有这个id的武器'
            await qc_test_wq.finish(msg, at_sender=True)
    else:
        msg = '请输入正确的数字'
        await qc_test_wq.finish(msg, at_sender=True)

qc_test_jn = on_command('Q技能')
qc_test_jn.handle()(check_user)


@qc_test_jn.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    num = await num_check(args)
    print(num)
    if num:
        result = DB.get_active_skill_by_id(int(num))
        if result:
            skill = ActiveSkill(result)

            msg = skill.get_skill_msg()
            await qc_test_jn.finish(msg, at_sender=True)

        else:
            msg = '没有这个id的技能'
            await qc_test_jn.finish(msg, at_sender=True)
    else:
        msg = '请输入正确的数字'
        await qc_test_wq.finish(msg, at_sender=True)


qc_start = on_command('Q宠创建')


@qc_start.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    user_id = int(event.user_id)
    group_id = int(event.group_id)
    result = DB.get_user_by_user_id(user_id)
    if result:
        msg = '你已经创建过Q宠了！'
        await qc_start.finish(msg, at_sender=True)
    else:
        user_info = Users(
            user_id=user_id,
            group_id=group_id,
            nick_name=user_id,
            power=random.randint(8, 10),
            agility=random.randint(8, 10),
            speed=random.randint(8, 10),
        )
        user_info.add()
        msg = '你已经成功创建Q宠，快 发送Q宠 查看吧！'
        await qc_start.finish(msg, at_sender=True)


qc_qc = on_command('Q宠切磋')
qc_qc.handle()(check_user)


@qc_qc.handle()
async def _(bot: Bot, event: MessageEvent,  args: Message = CommandArg()):
    at_qq = None  # 艾特的时候存到这里
    for arg in args:
        if arg.type == "at":
            at_qq = arg.data.get("qq", "")
    qc_qc.finish()
