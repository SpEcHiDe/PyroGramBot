# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright  https://en.m.wikipedia.org/wiki/Fair_use
from pyrogram import Client, filters
from pyrobot.helper_functions.cust_p_filters import sudo_filter


@Client.on_message(
    filters.command(["findbyfileid"]) &
    sudo_filter
)
async def fine_by_file_id(_, message):
    if not message.reply_to_message:
        return
    stickerid = str(message.reply_to_message.text)
    try:
        await message.reply_cached_media(
            stickerid,
            quote=True
        )
    except Exception as error:
        await message.reply_text(str(e), quote=True)
