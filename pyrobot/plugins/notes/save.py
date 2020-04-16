from pyrogram import (
    Client,
    Filters,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from pyrobot import (
    LOGGER,
    COMMAND_HAND_LER,
    DB_URI,
    TG_URI
)

if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.notes_sql as sql


from pyrobot.helper_functions.admin_check import AdminCheck
from pyrobot.helper_functions.msg_types import (
    get_note_type,
    get_file_id,
    Types
)


@Client.on_message(Filters.command("savenote", COMMAND_HAND_LER))
async def save_note(client, message):
    is_admin = await AdminCheck(
        client,
        message.chat.id,
        message.from_user.id
    )
    if not is_admin:
        return
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )
    if message.reply_to_message and message.reply_to_message.reply_markup is not None:
        fwded_mesg = await message.reply_to_message.forward(
            chat_id=TG_URI,
            disable_notification=True
        )
        chat_id = message.chat.id
        note_name = " ".join(message.command[1:])
        note_message_id = fwded_mesg.message_id
        sql.add_note_to_db(
            chat_id,
            note_name,
            note_message_id
        )
        await status_message.edit_text(
            f"note <u>{note_name}</u> added"
            # f"<a href='https://'>{message.chat.title}</a>"
        )
    else:
        note_name, text, data_type, content, buttons = get_note_type(message)

        if data_type is None:
            await status_message.edit_text("🤔 maybe note text is empty")
            return

        if not note_name:
            await status_message.edit_text("എന്തിന്ന് ഉള്ള മറുപടി ആണ് എന്ന് വ്യക്തം ആക്കിയില്ല 🤔")
            return

        # construct message using the above parameters
        fwded_mesg = None
        if data_type in (Types.BUTTON_TEXT, Types.TEXT):
            fwded_mesg = await client.send_message(
                chat_id=TG_URI,
                text=text,
                parse_mode="md",
                disable_web_page_preview=True,
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        elif data_type is not None:
            fwded_mesg = await client.send_cached_media(
                chat_id=TG_URI,
                file_id=content,
                caption=text,
                parse_mode="md",
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        # save to db 🤔
        if fwded_mesg is not None:
            chat_id = message.chat.id
            note_message_id = fwded_mesg.message_id
            sql.add_note_to_db(
                chat_id,
                note_name,
                note_message_id
            )
            await status_message.edit_text(
                f"note <u>{note_name}</u> added"
                # f"<a href='https://'>{message.chat.title}</a>"
            )
        else:
            await status_message.edit_text("🥺 this might be an error 🤔")