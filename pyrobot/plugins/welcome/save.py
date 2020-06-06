from pyrogram import (
    Client,
    Filters,
    InlineKeyboardMarkup
)

from pyrobot import (
    COMMAND_HAND_LER,
    DB_URI,
    TG_URI
)

from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.msg_types import (
    get_note_type,
    Types
)
if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.welcome_sql as sql


@Client.on_message(Filters.command(["savewelcome", "setwelcome"], COMMAND_HAND_LER))
async def save_note(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )
    if len(message.command) == 2:
        chat_id = message.chat.id
        note_message_id = int(message.command[1])
        sql.add_welcome_setting(
            chat_id,
            True,
            0,
            note_message_id
        )
        await status_message.edit_text(
            "welcome message saved"
        )
    elif message.reply_to_message and message.reply_to_message.reply_markup is not None:
        fwded_mesg = await message.reply_to_message.forward(
            chat_id=TG_URI,
            disable_notification=True
        )
        chat_id = message.chat.id
        note_message_id = fwded_mesg.message_id
        sql.add_welcome_setting(
            chat_id,
            True,
            0,
            note_message_id
        )
        await status_message.edit_text(
            "welcome message saved"
        )
    else:
        note_name, text, data_type, content, buttons = get_note_type(message, 1)

        if data_type is None:
            await status_message.edit_text("🤔 maybe welcome text is empty")
            return

        # construct message using the above parameters
        fwded_mesg = None
        reply_markup = None
        if len(buttons) > 0:
            reply_markup = InlineKeyboardMarkup(buttons)
        if data_type in (Types.BUTTON_TEXT, Types.TEXT):
            fwded_mesg = await client.send_message(
                chat_id=TG_URI,
                text=text,
                parse_mode="md",
                disable_web_page_preview=True,
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=reply_markup
            )
        elif data_type is not None:
            fwded_mesg = await client.send_cached_media(
                chat_id=TG_URI,
                file_id=content,
                caption=text,
                parse_mode="md",
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=reply_markup
            )

        # save to db 🤔
        if fwded_mesg is not None:
            chat_id = message.chat.id
            note_message_id = fwded_mesg.message_id
            sql.add_welcome_setting(
                chat_id,
                bool(note_name),
                0,
                note_message_id
            )
            await status_message.edit_text(
                "welcome message saved"
            )
