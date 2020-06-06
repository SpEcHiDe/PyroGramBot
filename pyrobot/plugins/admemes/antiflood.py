"""Set Antiflood
Syntax: .setflood"""

import asyncio

from pyrogram import (
    ChatPermissions,
    Client,
    Filters
)
from pyrobot import (
    COMMAND_HAND_LER,
    DB_URI
)

from pyrobot.helper_functions.admin_check import admin_check
if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.antiflood_sql as sql
    CHAT_FLOOD = sql.__load_flood_settings()


@Client.on_message(group=1)
async def check_flood(client, message):
    """ check all messages """
    if DB_URI is None:
        return
    #
    if not CHAT_FLOOD:
        return
    if not str(message.chat.id) in CHAT_FLOOD:
        return
    is_admin = await admin_check(message)
    if is_admin:
        return
    should_ban = sql.update_flood(message.chat.id, message.from_user.id)
    if not should_ban:
        return
    try:
        await message.chat.restrict_member(
            user_id=message.from_user.id,
            permissions=ChatPermissions(
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        no_admin_privilege_message = await message.reply_text(
            text="""<b>Automatic AntiFlooder</b>
@admin <a href='tg://user?id={}'>{}</a> is flooding this chat.

`{}`""".format(message.from_user.id, message.from_user.first_name, str(e))
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit_text(
            text="https://t.me/c/1092696260/724970",
            disable_web_page_preview=True
        )
    else:
        await client.send_message(
            chat_id=message.chat.id,
            text="""<b>Automatic AntiFlooder</b>
<a href='tg://user?id={}'>{}</a> has been automatically restricted
because he reached the defined flood limit.

#FLOOD""".format(
    message.from_user.id,
    message.from_user.first_name
),
            reply_to_message_id=message.message_id
        )


@Client.on_message(Filters.command("setflood", COMMAND_HAND_LER))
async def set_flood(_, message):
    """ /setflood command """
    is_admin = await admin_check(message)
    if not is_admin:
        return
    if len(message.command) == 2:
        input_str = message.command[1]
    try:
        sql.set_flood(message.chat.id, input_str)
        global CHAT_FLOOD
        CHAT_FLOOD = sql.__load_flood_settings()
        await message.reply_text(
            "Antiflood updated to {} in the current chat".format(input_str)
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await message.reply_text(str(e))


@Client.on_message(Filters.command("flood", COMMAND_HAND_LER))
async def get_flood_settings(_, message):
    flood_limit = get_flood_limit(message.chat.id)
    await message.reply_text(
        "<b>This chat is</b> currently "
        "enforcing <i>flood control</i> after "
        f"<code>{flood_limit}</code> messages. "
        "⚠️⚠️ <u><i>Any users sending more than that amount of messages "
        "will be muted.</i></u>"
    )
