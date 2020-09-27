import re
from pyrogram import filters
from pyrogram.types import Message
from pyrobot import (
    TG_URI
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.msg_types import (
    get_file_id
)


@PyroBot.on_message(
    filters.incoming,
    group=2
)
async def watch_all_messages(client: PyroBot, message: Message):
    to_match = message.text or message.caption or ""
    flt_list = client.filterstore.get(str(message.chat.id), [])
    for flt in flt_list:
        pattern = r"( |^|[^\w])" + re.escape(flt) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            flt_message = await client.get_messages(
                chat_id=TG_URI,
                message_ids=flt_list[flt],
                replies=0
            )
            n_m = message
            if message.reply_to_message:
                n_m = message.reply_to_message
            # 🥺 check two conditions 🤔🤔
            if flt_message.media:
                _, file_id = get_file_id(flt_message)
                caption = flt_message.caption
                if caption:
                    caption = caption.html
                if not caption:
                    caption = ""
                await n_m.reply_cached_media(
                    file_id=file_id,
                    caption=caption,
                    parse_mode="html",
                    reply_markup=flt_message.reply_markup
                )
            else:
                caption = flt_message.text
                if caption:
                    caption = caption.html
                if not caption:
                    caption = ""
                disable_web_page_preview = True
                if "gra.ph" in caption or "youtu" in caption:
                    disable_web_page_preview = False
                await n_m.reply_text(
                    text=caption,
                    disable_web_page_preview=disable_web_page_preview,
                    parse_mode="html",
                    reply_markup=flt_message.reply_markup
                )
            break
