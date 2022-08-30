import os
import shutil
from pyrogram import Client, filters
from telegraph import upload_file
from pyrobot import TMP_DOWNLOAD_DIRECTORY, TE_LEGRA_PH_DOMAIN
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.get_file_id import get_file_id


@Client.on_message(
    filters.command([
        "telegraph",
        "graphorg",
    ]) & sudo_filter
)
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("Reply to a supported media file")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await message.reply_text("Not supported!")
        return
    _t = os.path.join(TMP_DOWNLOAD_DIRECTORY, str(replied.id))
    if not os.path.isdir(_t):
        os.makedirs(_t)
    _t += "/"
    download_location = await replied.download(_t)
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply_text(message, text=document)
    else:
        await message.reply(
            f"{TE_LEGRA_PH_DOMAIN}{response[0]}", disable_web_page_preview=True
        )
    finally:
        shutil.rmtree(_t, ignore_errors=True)
