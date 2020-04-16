from pyrogram import (
    Client,
    Filters
)

from pyrobot import (
    LOGGER,
    COMMAND_HAND_LER,
    DB_URI,
    TG_URI
)

if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.notes_sql as sql

from pyrobot.helper_functions.msg_types import (
    get_file_id
)


async def get_note_with_command(message, note_name):
    note_d = sql.get_note(message.chat.id, note_name)
    note_message_id = note_d.d_message_id
    note_message = await message._client.get_messages(
        chat_id=TG_URI,
        message_ids=note_message_id,
        replies=0
    )
    n_m = message
    if message.reply_to_message:
        n_m = message.reply_to_message
    # 🥺 check two conditions 🤔🤔
    if note_message.media:
        _, file_id = get_file_id(note_message)
        await n_m.reply_cached_media(
            file_id=file_id,
            caption=note_message.caption.html,
            parse_mode="html",
            reply_markup=note_message.reply_markup
        )
    else:
        disable_web_page_preview = True
        await n_m.reply_text(
            text=note_message.text.html,
            disable_web_page_preview=disable_web_page_preview,
            parse_mode="html",
            reply_markup=note_message.reply_markup
        )


@Client.on_message(Filters.command("getnote", COMMAND_HAND_LER))
async def get_note(client, message):
    note_name = " ".join(message.command[1:])
    await get_note_with_command(message, note_name)