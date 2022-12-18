# credits: https://github.com/SpEcHiDe/PyroGramBot/pull/34

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import admin_fliter


@Client.on_message(filters.command(["pin"], COMMAND_HAND_LER) & admin_fliter)
async def pin(_, message: Message):
    if not message.reply_to_message:
        return
    args = message.text.lower().split()
    notify = not any(arg in args for arg in ('loud', 'notify'))
    await message.reply_to_message.pin(disable_notification=notify)


@Client.on_message(filters.command(["unpin"], COMMAND_HAND_LER) & admin_fliter)
async def unpin(_, message: Message):
    if not message.reply_to_message:
        return
    await message.reply_to_message.unpin()
