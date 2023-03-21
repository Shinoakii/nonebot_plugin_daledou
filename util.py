from .database.db import DB
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
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
