import zlib
import random
from nonebot import on_command, rule
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import Permission
from nonebot.log import logger, default_format
from nonebot.matcher import FinishedException

enc = on_command(("nya", "encode"), aliases=set([("nya", "e"), ("喵", "e")]))
dec = on_command(("nya", "decode"), aliases=set([("nya", "d"), ("喵", "d")]))


@enc.handle()
async def enc_handle(bot: Bot, event: Event, state: T_State):
    orig = str(event.get_message()).strip()
    if orig:
        state["orig"] = orig


@enc.got("orig", prompt="你想要加密什么（")
async def enc_process(bot: Bot, event: Event, state: T_State):
    if len(state["orig"]) > 20:
        await enc.send(random.choices(["呜呜呜 太大了塞不下啊x",
                                      "好长 咱搞不定x"], [1, 49])[0])
        await enc.finish("咱最长只能处理 20 个字符 这里建议换个短点的试试（")

    orig = state["orig"]
    logger.debug(str(int.from_bytes(bytes(orig, "utf-8"), "little")) +
                 " -> " + bin(int.from_bytes(bytes(orig, "utf-8"), "little")))
    await enc.send(bin(int.from_bytes(bytes(orig, "utf-8"), "little"))[2:]
                   .replace('1', '喵').replace('0', '呜'))


@dec.handle()
async def dec_handle(bot: Bot, event: Event, state: T_State):
    en = str(event.get_message()).strip()
    if en:
        state["en"] = en


@dec.got("en", prompt="你这是要解密空气？")
async def dec_process(bot: Bot, event: Event, state: T_State):
    en = state["en"]
    # Sanity Check
    if(len(en) % 8):
        logger.info("User entered a string with length " +
                    str(len(en))+", rejected")
        if(len(en) < 8):
            await dec.finish(random.choices(["你这也太短了 没劲x",
                                             "好短 你这喵语有问题啊（"], [1, 49])[0])
        else:
            await dec.finish("你是不是漏了什么，这不对劲啊x")
    cset = set(en)
    if(not cset.issubset(set("喵呜"))):
        cset.discard("喵")
        cset.discard("呜")
        msgtmp = "User entered a string with characters other than 喵 & 呜, namely "
        for x in cset:
            msgtmp += x + ", "
        logger.info(msgtmp[:-2])
        await dec.finish("这喵语里面混进了奇怪的东西x")

    conv = int(en.replace('喵', '1').replace('呜', '0'), 2)
    try:
        await dec.send("加密的内容是：\n"
                       + str(conv.to_bytes(150, "little"), "utf-8"))
    except UnicodeDecodeError as e:
        logger.info(e+" when decoding " + bin(conv))
        await dec.send("（抬手，指）你这喵语有问题啊")
    except Exception as e:
        logger.error(e+" when decoding " + bin(conv))
        await dec.finish("这是啥东西，，\nError: "+e)
