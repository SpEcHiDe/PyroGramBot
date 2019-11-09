"""Set Antiflood
Syntax: .setflood"""

import asyncio

from pyrogram import Client, Filters
from pyrobot import COMMAND_HAND_LER, DB_URI

if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.antiflood_sql as sql
    CHAT_FLOOD = sql.__load_flood_settings()


@Client.on_message(group=1)
async def check_flood(client, message):
    if DB_URI is None:
        return
    # logger.info(CHAT_FLOOD)
    if not CHAT_FLOOD:
        return
    if not (str(message.chat.id) in CHAT_FLOOD):
        return
    # TODO: exempt admins from this
    should_ban = sql.update_flood(message.chat.id, message.from_user.id)
    if not should_ban:
        return
    try:
        await client.kick_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            until_date=31
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        no_admin_privilege_message = await client.send_message(
            chat_id=message.chat.id,
            text="""**Automatic AntiFlooder**
@admin [User](tg://user?id={}) is flooding this chat.

`{}`""".format(message.from_user.id, str(e)),
            reply_to_message_id=message.message_id
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit_text(
            text="https://t.me/keralagram/724970",
            disable_web_page_preview=True
        )
    else:
        await client.send_message(
            chat_id=message.chat.id,
            text="""**Automatic AntiFlooder**
[User](tg://user?id={}) has been automatically restricted
because he reached the defined flood limit.""".format(message.from_user.id),
            reply_to_message_id=message.message_id
        )


@Client.on_message(Filters.command("setflood", COMMAND_HAND_LER)  & Filters.me)
async def set_flood(client, message):
    if len(message.command) == 2:
        input_str = message.command[1]
    try:
        sql.set_flood(message.chat.id, input_str)
        CHAT_FLOOD = sql.__load_flood_settings()
        await message.edit_text(
            "Antiflood updated to {} in the current chat".format(input_str)
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await message.edit_text(str(e))
