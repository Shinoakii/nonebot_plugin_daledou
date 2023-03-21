from .database.db import DB
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent
)
from nonebot.exception import FinishedException


async def check_user(
    bot: Bot,
    event: MessageEvent,
):
    user_id = event.user_id
    user = DB.get_user_by_user_id(user_id)
    if not user:
        await bot.send(event, "您还未创建Q宠，请发送Q宠创建")
        raise FinishedException


async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    name: str,  # 转发的用户名称
    uin: str,  # qq
    msgs: list  # 转发内容
):
    """合并消息转发"""
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )


async def send_forward_msg_list(
    bot: Bot,
    event: MessageEvent,
    # 格式[*dict] 例[*{"type": "node", "data": {"name": name, "uin": uin, "content": msg}}]
    messages: list,
):
    """
    合并消息转发
    区分人
    """

    if isinstance(event, GroupMessageEvent):
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
