"""ThumbNail utilities, © @AnyDLBot
Available Commands:
.savethumbnail
.clearthumbnail
.getthumbnail"""

from pyrogram import Client, Filters

import os
import time
from datetime import datetime

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image


thumb_image_path = TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@Client.on_message(Filters.command("savethumbnail", COMMAND_HAND_LER)  & Filters.me)
async def save_thumb_nail(client, message):
    await message.edit("processing ...")
    if message.reply_to_message is not None:
        if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        start_t = datetime.now()
        download_location = TMP_DOWNLOAD_DIRECTORY + "/"
        c_time = time.time()
        downloaded_file_name = await client.download_media(
            message=message.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                "trying to download", message.message_id, message.chat.id, c_time
            )
        )
        end_t = datetime.now()
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = 0
        if metadata.has("height"):
            height = metadata.get("height")
        # resize image
        # ref: https://t.me/PyrogramChat/44663
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        img = Image.open(downloaded_file_name)
        # https://stackoverflow.com/a/37631799/4723940
        # img.thumbnail((320, 320))
        img.resize((320, height))
        img.save(thumb_image_path, "JPEG")
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await message.edit(
            "Custom video / file thumbnail saved. " + \
            "This image will be used in the upload, till `.clearthumbnail`."
        )
    else:
        await message.edit("Reply to a photo to save custom thumbnail")


@Client.on_message(Filters.command("clearthumbnail", COMMAND_HAND_LER)  & Filters.me)
async def save_thumb_nail(client, message):
    await message.edit("processing ...")
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await message.edit("✅ Custom thumbnail cleared succesfully.")


@Client.on_message(Filters.command("getthumbnail", COMMAND_HAND_LER)  & Filters.me)
async def save_thumb_nail(client, message):
    await message.edit("processing ...")
    """if message.reply_to_message is not None:
        reply_to_message = message.reply_to_message
        if reply_to_message.document is not None:
            await client.send_document(
                chat_id=message.chat.id,
                document=reply_to_message.document.thumbs[0].file_id,
                disable_notification=True,
                reply_to_message_id=message.message_id
            )
        if reply_to_message.video is not None:
            await client.send_document(
                chat_id=message.chat.id,
                document=reply_to_message.video.thumbs[0].file_id,
                disable_notification=True,
                reply_to_message_id=message.message_id
            )
        await message.delete()
    el"""
    if os.path.exists(thumb_image_path):
        caption_str = "Currently Saved Thumbnail. Clear with `.clearthumbnail`"
        await client.send_document(
            chat_id=message.chat.id,
            document=thumb_image_path,
            caption=caption_str,
            disable_notification=True,
            reply_to_message_id=message.message_id
        )
        await message.edit(caption_str)
    else:
        await message.edit("Reply `.gethumbnail` as a reply to a media")
