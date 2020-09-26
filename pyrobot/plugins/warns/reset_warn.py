import json
import time
from pyrogram import filters
from pyrogram.types import (
    Message, CallbackQuery, ChatPermissions,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrobot import (
    COMMAND_HAND_LER,
    WARN_DATA_ID
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.cust_p_filters import (
    admin_fliter,
    f_onw_fliter
)


@PyroBot.on_message(
    filters.command(["resetwarn"], COMMAND_HAND_LER) &
    admin_fliter &
    f_onw_fliter
)
async def reset_all_warns(client: PyroBot, msg: Message):
    replied = msg.reply_to_message
    if not replied:
        return
    user_id = replied.from_user.id
    if replied.from_user.is_self:
        return
    chat_id = msg.chat.id
    if chat_id not in client.warndatastore:
        client.warndatastore[chat_id] = {}
    DATA = client.warndatastore[chat_id]
    if DATA.get(user_id):
        DATA.pop(user_id)
        await msg.reply("All Warns are removed for this User.")
    else:
        await msg.reply("User already not have any warn.")
    client.warndatastore[chat_id] = DATA
    await client.save_public_store(
        WARN_DATA_ID,
        json.dumps(client.warndatastore)
    )

