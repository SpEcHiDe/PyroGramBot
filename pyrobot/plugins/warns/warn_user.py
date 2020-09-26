import json
import time
from pyrogram import filters
from pyrogram.types import (
    Message, CallbackQuery, ChatPermissions,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from pyrobot import (
    COMMAND_HAND_LER,
    WARN_DATA_ID,
    WARN_SETTINGS_ID
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.cust_p_filters import (
    admin_fliter,
    f_onw_fliter
)


@PyroBot.on_message(
    filters.command(["warnuser", "warn"], COMMAND_HAND_LER) &
    admin_fliter &
    f_onw_fliter
)
async def warn_user(client: PyroBot, msg: Message):
    chat_id = msg.chat.id

    replied = msg.reply_to_message
    if not replied:
        return
    
    if chat_id not in client.warndatastore:
        client.warndatastore[chat_id] = {}

    DATA = client.warndatastore[chat_id]

    user_id = replied.from_user.id
    mention = f"<a href='tg://user?id={user_id}'>{replied.from_user.first_name}</a>"

    if replied.from_user.is_self:
        await msg.reply_text("ഞാൻ സ്വയം താക്കീത്‌ നൽകാൻ പോകുന്നില്ല")
        return

    if await admin_check(replied):
        await msg.reply("User is Admin, Cannot Warn.")
        return

    if len(msg.command) < 2:
        await msg.reply("`Give a reason to warn him.`")
        return

    _, reason = msg.text.split(maxsplit=1)

    if chat_id not in client.warnsettingsstore:
        client.warnsettingsstore[chat_id] = {
            "WARN_LIMIT": 5,
            "WARN_MODE": "kick"
        }
    w_s = client.warnsettingsstore[chat_id]
    w_l = w_s["WARN_LIMIT"]
    w_m = w_s["WARN_MODE"]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "ഈ താക്കീത്‌ നീക്കംചെയ്യുക",
            callback_data=f"rmwarn_{user_id}_{msg.from_user.id}"
        )]
    ])

    if not DATA.get(user_id):
        w_d = {
            "limit": 1,
            "reason": [reason]
        }
        DATA[user_id] = w_d  # warning data
        reply_text = f"#Warned\n{mention} has 1/{w_l} warnings.\n"
        reply_text += f"<u>Reason</u>: {reason}"
        await replied.reply_text(reply_text, reply_markup=keyboard)
    else:
        p_l = DATA[user_id]["limit"]  # previous limit
        nw_l = p_l + 1  # new limit
        if nw_l >= w_l:
            if w_m == "ban":
                await msg.chat.kick_member(user_id)
                exec_str = "BANNED"
            elif w_m == "kick":
                await msg.chat.kick_member(
                    user_id,
                    until_date=time.time() + 61
                )
                exec_str = "KICKED"
            elif w_m == "mute":
                await msg.chat.restrict_member(user_id, ChatPermissions())
                exec_str = "MUTED"
            reason = ("\n".join(DATA[user_id]["reason"]) + "\n" + str(reason))
            await msg.reply(
                f"#WARNED_{exec_str}\n"
                f"{exec_str} User: {mention}\n"
                f"Warn Counts: {w_l}/{w_l} Warnings\n"
                f"Reason: {reason}"
            )
            DATA.pop(user_id)

        else:
            DATA[user_id]["limit"] = nw_l
            DATA[user_id]["reason"].append(reason)
            r_t = f"#Warned\n{mention} has {nw_l}/{w_l} warnings.\n"
            r_t += f"<u>Reason</u>: {reason}"   # r_t = reply text
            await replied.reply_text(r_t, reply_markup=keyboard)
    
    client.warndatastore[chat_id] = DATA
    await client.save_public_store(
        WARN_DATA_ID,
        json.dumps(client.warndatastore)
    )
    client.warnsettingsstore[chat_id] = w_s
    await client.save_public_store(
        WARN_SETTINGS_ID,
        json.dumps(client.warnsettingsstore)
    )
