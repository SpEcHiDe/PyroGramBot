from pyrogram import (
    Client,
    filters
)
from pyrobot import (
    COMMAND_HAND_LER,
    DB_URI,
    TG_URI
)
from pyrobot.helper_functions.msg_types import (
    get_file_id
)
if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.notes_sql as sql


async def get_note_with_command(message, note_name):
    note_d = sql.get_note(message.chat.id, note_name)
    if not note_d:
        return
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
        caption = note_message.caption
        if caption:
            caption = caption.html
        await n_m.reply_cached_media(
            file_id=file_id,
            caption=caption,
            parse_mode="html",
            reply_markup=note_message.reply_markup
        )
    else:
        caption = note_message.text
        if caption:
            caption = caption.html
        disable_web_page_preview = True
        if "gra.ph" in caption or "youtu" in caption:
            disable_web_page_preview = False
        await n_m.reply_text(
            text=caption,
            disable_web_page_preview=disable_web_page_preview,
            parse_mode="html",
            reply_markup=note_message.reply_markup
        )


@Client.on_message(
    filters.command(["getnote", "get"], COMMAND_HAND_LER) &
    filters.incoming
)
async def get_note(_, message):
    note_name = " ".join(message.command[1:])
    await get_note_with_command(message, note_name)


@Client.on_message(
    filters.regex(pattern=r"#(\w+)") &
    filters.incoming
)
async def get_hash_tag_note(_, message):
    note_name = message.matches[0].group(1)
    await get_note_with_command(message, note_name)
