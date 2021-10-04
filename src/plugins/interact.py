import random
import re
from nonebot import on_regex, rule
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import Permission
from nonebot.adapters import cqhttp as cq

nya = on_regex(r"^[ 　\n]*喵[喵呜]*")
wei = on_regex(r"^[ 　\n]*wei[ ,，\n]+zaima", re.I)
caress = on_regex(r"^[ 　\n]*[摸揉搓]+", rule=rule.to_me())
hug = on_regex(r"^[ 　\n]*(抱|贴)+", rule=rule.to_me())


@nya.handle()
async def nya_handle(bot: Bot, event: Event, state: T_State):
    msg = "喵"
    ch = ['喵', '呜']
    ending = ['！', '', 'x', '（']
    for i in range(random.randint(0, 5)):
        msg += random.choice(ch)
    msg += random.choices(ending, [1, 6, 1, 2])[0]
    await bot.send(event, msg)


@wei.handle()
async def wei_handle(bot: Bot, event: Event, state: T_State):
    await bot.send(event, random.choice(["buzai", "buzai, cmn", "buzai, cnm"]))


@caress.handle()
async def caress_handle(bot: Bot, event: Event, state: T_State):
    await bot.send(event, random.choice(["揉揉喵", "揉揉", "揉",
                                         "摸摸", "摸摸喵",
                                         "搓搓", "搓搓喵"])
                   + random.choices(["", "（", "x"], [2, 2, 1])[0], at_sender=True)


@hug.handle()
async def hug_handle(bot: Bot, event: Event, state: T_State):
    await bot.send(event, random.choice(["抱抱", "抱", "抱住", "贴贴"])
                   + random.choice(["", "喵"])
                   + random.choices(["", "（", "x"], [2, 2, 1])[0], at_sender=True)
