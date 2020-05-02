"""Upload Local Media to Telegram
Syntax: .upload* *"""

import os
import time
from datetime import datetime

from pyrogram import (
    Client,
    Filters
)

from pyrobot import (
    COMMAND_HAND_LER,
    TMP_DOWNLOAD_DIRECTORY
)
from pyrobot.helper_functions.check_if_thumb_exists import is_thumb_image_exists
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.display_progress_dl_up import progress_for_pyrogram


@Client.on_message(Filters.command("uploadasdoc", COMMAND_HAND_LER)  & sudo_filter)
async def upload_as_document(client, message):
    status_message = await message.reply_text("...")
    if " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        if os.path.exists(local_file_name):
            thumb_image_path = await is_thumb_image_exists(local_file_name)
            start_t = datetime.now()
            c_time = time.time()
            doc_caption = os.path.basename(local_file_name)
            await message.reply_document(
                document=local_file_name,
                thumb=thumb_image_path,
                caption=doc_caption,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", status_message, c_time
                )
            )
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await status_message.edit(f"Uploaded in {ms} seconds")
        else:
            await status_message.edit("404: media not found")
    else:
        await status_message.edit(f"<code>{COMMAND_HAND_LER}uploadasdoc FILE_PATH</code> to upload to current Telegram chat")



@Client.on_message(Filters.command("uploadasvideo", COMMAND_HAND_LER)  & sudo_filter)
async def upload_as_video(client, message):
    status_message = await message.reply_text("...")
    if " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        if os.path.exists(local_file_name):
            thumb_image_path = await is_thumb_image_exists(local_file_name)
            start_t = datetime.now()
            c_time = time.time()
            doc_caption = os.path.basename(local_file_name)
            await message.reply_video(
                video=local_file_name,
                caption=doc_caption,
                parse_mode="html",
                # duration=,
                # width=,
                # height=,
                thumb=thumb_image_path,
                supports_streaming=True,
                disable_notification=True,
                reply_to_message_id=message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", status_message, c_time
                )
            )
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await status_message.edit(f"Uploaded in {ms} seconds")
        else:
            await status_message.edit("404: media not found")
    else:
        await status_message.edit(f"<code>{COMMAND_HAND_LER}uploadasvideo FILE_PATH</code> to upload to current Telegram chat")



@Client.on_message(Filters.command("uploadasphoto", COMMAND_HAND_LER)  & sudo_filter)
async def upload_as_photo(client, message):
    status_message = await message.reply_text("...")
    if " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        thumb_image_path = await is_thumb_image_exists(local_file_name)
        if os.path.exists(local_file_name):
            start_t = datetime.now()
            c_time = time.time()
            doc_caption = os.path.basename(local_file_name)
            await message.reply_photo(
                photo=local_file_name,
                caption=doc_caption,
                parse_mode="html",
                # ttl_seconds=,
                disable_notification=True,
                reply_to_message_id=message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", status_message, c_time
                )
            )
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await status_message.edit(f"Uploaded in {ms} seconds")
        else:
            await status_message.edit("404: media not found")
    else:
        await status_message.edit(f"<code>{COMMAND_HAND_LER}uploadasphoto FILE_PATH</code> to upload to current Telegram chat")
