"""Download Telegram Media
Syntax: .download"""

from pyrogram import Client, Filters

import os
import time
from datetime import datetime

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY
from pyrobot.helper_functions.display_progress_dl_up import progress_for_pyrogram


@Client.on_message(Filters.command("download", COMMAND_HAND_LER)  & Filters.me)
async def down_load_media(client, message):
    if message.reply_to_message is not None:
        if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        start_t = datetime.now()
        download_location = TMP_DOWNLOAD_DIRECTORY + "/"
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=message.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                "trying to download", message, c_time
            )
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await message.edit(f"Downloaded to {the_real_download_location} in {ms} seconds")
    else:
        await message.edit("Reply to a Telegram Media, to download it to local server.")
