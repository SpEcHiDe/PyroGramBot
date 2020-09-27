from pyrogram import (
    filters
)
from pyrobot import (
    DB_URI,
    TG_URI
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.msg_types import (
    get_file_id
)
from pyrobot.helper_functions.string_handling import (
    format_welcome_caption
)
if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.welcome_sql as sql


async def delete_prev_welcome(message, previous_w_message_id):
    await message._client.delete_messages(
        chat_id=message.chat.id,
        message_ids=previous_w_message_id,
        revoke=True
    )


async def get_note_with_command(message):
    note_d = sql.get_current_welcome_settings(message.chat.id)
    if not note_d:
        return
    #
    note_message_id = int(note_d.f_mesg_id)
    note_message = await message._client.get_messages(
        chat_id=TG_URI,
        message_ids=note_message_id,
        replies=0
    )
    n_m = message
    # 🥺 check two conditions 🤔🤔
    for c_m in message.new_chat_members:
        if note_d.should_clean_welcome:
            await delete_prev_welcome(message, int(note_d.previous_welcome))
        if note_message.media:
            _, file_id = get_file_id(note_message)
            caption = note_message.caption
            if caption:
                caption = format_welcome_caption(caption.html, c_m)
            n_m = await n_m.reply_cached_media(
                file_id=file_id,
                caption=caption,
                parse_mode="html",
                reply_markup=note_message.reply_markup
            )
        else:
            caption = note_message.text
            if caption:
                caption = format_welcome_caption(caption.html, c_m)
            disable_web_page_preview = True
            if "gra.ph" in caption or "youtu" in caption:
                disable_web_page_preview = False
            n_m = await n_m.reply_text(
                text=caption,
                disable_web_page_preview=disable_web_page_preview,
                parse_mode="html",
                reply_markup=note_message.reply_markup
            )
        #
        sql.update_previous_welcome(message.chat.id, n_m.message_id)


@PyroBot.on_message(filters.new_chat_members)
async def new_welcome(_, message):
    await get_note_with_command(message)
