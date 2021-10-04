# Copied from https://github.com/SK-415/HarukaBot/blob/master/src/plugins/haruka_bot/plugins/auto_agree.py
# Redid wording

from nonebot import on_request
from nonebot.adapters.cqhttp import Bot, FriendRequestEvent, GroupRequestEvent
from nonebot.typing import T_State


friend_req = on_request(priority=5)


@friend_req.handle()
async def friend_accept(bot: Bot, event: FriendRequestEvent, state: T_State):
    if str(event.user_id) in bot.config.superusers:
        await bot.set_friend_add_request(flag=event.flag, approve=True)


group_invite = on_request(priority=5)


@group_invite.handle()
async def group_accept(bot: Bot, event: GroupRequestEvent, state: T_State):
    if (event.sub_type == 'invite' and
            str(event.user_id) in bot.config.superusers):
        await bot.set_group_add_request(flag=event.flag, sub_type='invite',
                                        approve=True)
