from pyrogram import filters
from pyrogram.types import Message
from pyrobot import COMMAND_HAND_LER
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.cust_p_filters import admin_fliter


@PyroBot.on_message(filters.command(["warns"], COMMAND_HAND_LER) & admin_fliter)
async def check_warns_of_user(client: PyroBot, msg: Message):
    replied = msg.reply_to_message
    if not replied:
        return

    chat_id = str(msg.chat.id)
    if chat_id not in client.warndatastore:
        client.warndatastore[chat_id] = {}
    DATA = client.warndatastore[chat_id]
    W_S = client.warnsettingsstore[chat_id]
    WARN_LIMIT = W_S["WARN_LIMIT"]

    user_id = str(replied.from_user.id)
    mention = f"<a href='tg://user?id={user_id}'>"
    mention += replied.from_user.first_name
    mention += "</a>"

    if replied.from_user.is_self:
        return

    if DATA.get(user_id):
        w_c = DATA[user_id]["limit"]  # warn counts
        reason = "\n".join(DATA[user_id]["reason"])
        reply_msg = (
            "#WARNINGS\n"
            f"User: {mention}\n"
            f"Warn Counts: {w_c}/{WARN_LIMIT} Warnings\n"
            f"Reason: {reason}"
        )
        await msg.reply(reply_msg)
    else:
        await msg.reply("Warnings not Found.")
