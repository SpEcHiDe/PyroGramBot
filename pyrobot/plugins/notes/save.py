from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrobot import COMMAND_HAND_LER, DB_URI, TG_URI
from pyrobot.helper_functions.cust_p_filters import admin_fliter
from pyrobot.helper_functions.msg_types import get_note_type, Types

if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.notes_sql as sql


@Client.on_message(
    filters.command(["savenote", "save"], COMMAND_HAND_LER) & admin_fliter
)
async def save_note(client, message):
    status_message = await message.reply_text("checking 🤔🙄🙄", quote=True)
    if message.reply_to_message and message.reply_to_message.reply_markup is not None:
        fwded_mesg = await message.reply_to_message.forward(
            chat_id=TG_URI, disable_notification=True
        )
        chat_id = message.chat.id
        note_name = " ".join(message.command[1:])
        note_message_id = fwded_mesg.id
        sql.add_note_to_db(chat_id, note_name, note_message_id)
        await status_message.edit_text(
            f"note <u>{note_name}</u> added"
            # f"<a href='https://'>{message.chat.title}</a>"
        )
    else:
        note_name, text, data_type, content, buttons = get_note_type(message, 2)

        if data_type is None:
            await status_message.edit_text("🤔 maybe note text is empty")
            return

        if not note_name:
            await status_message.edit_text(
                "എന്തിന്ന് ഉള്ള മറുപടി ആണ് എന്ന് വ്യക്തം ആക്കിയില്ല 🤔"
            )
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
                disable_web_page_preview=True,
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=reply_markup,
            )
        elif data_type is not None:
            fwded_mesg = await client.send_cached_media(
                chat_id=TG_URI,
                file_id=content,
                caption=text,
                disable_notification=True,
                reply_to_message_id=1,
                reply_markup=reply_markup,
            )

        # save to db 🤔
        if fwded_mesg is not None:
            chat_id = message.chat.id
            note_message_id = fwded_mesg.id
            sql.add_note_to_db(chat_id, note_name, note_message_id)
            await status_message.edit_text(
                f"note <u>{note_name}</u> added"
                # f"<a href='https://'>{message.chat.title}</a>"
            )
        else:
            await status_message.edit_text("🥺 this might be an error 🤔")
