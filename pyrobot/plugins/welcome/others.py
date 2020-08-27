from pyrogram import (
    Client,
    filters
)
from pyrobot import (
    COMMAND_HAND_LER,
    DB_URI,
    MAX_MESSAGE_LENGTH
)
from pyrobot.helper_functions.admin_check import admin_check
if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.welcome_sql as sql


@Client.on_message(
    filters.command(["clearwelcome", "resetwelcome"], COMMAND_HAND_LER)
)
async def clear_note(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )
    sql.rm_welcome_setting(message.chat.id)
    await status_message.edit_text(
        "welcome message cleared from current chat."
    )
