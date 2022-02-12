"""ThumbNail utilities, © @AnyDLBot
Available Commands:
.savethumbnail
.clearthumbnail
.getthumbnail"""

import os
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram import Client, filters
from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot.helper_functions.display_progress_dl_up import progress_for_pyrogram


thumb_image_path = TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@Client.on_message(filters.command("savethumbnail", COMMAND_HAND_LER) & sudo_filter)
async def save_thumb_nail(client, message):
    status_message = await message.reply_text("...")
    if message.reply_to_message is not None:
        if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        download_location = TMP_DOWNLOAD_DIRECTORY + "/"
        c_time = time.time()
        downloaded_file_name = await client.download_media(
            message=message.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=("trying to download", status_message, c_time),
        )
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = 0
        if metadata.has("height"):
            height = metadata.get("height")
        # resize image
        # ref: https://t.me/PyrogramChat/44663
        img = Image.open(downloaded_file_name)
        # https://stackoverflow.com/a/37631799/4723940
        # img.thumbnail((320, 320))
        img.resize((320, height))
        img.save(thumb_image_path, "JPEG")
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await status_message.edit(
            "Custom video / file thumbnail saved. "
            "This image will be used in the upload, "
            "till <code>.clearthumbnail</code>."
        )
    else:
        await status_message.edit("Reply to a photo to save custom thumbnail")


@Client.on_message(filters.command("clearthumbnail", COMMAND_HAND_LER) & sudo_filter)
async def clear_thumb_nail(client, message):
    status_message = await message.reply_text("...")
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await status_message.edit("✅ Custom thumbnail cleared succesfully.")


@Client.on_message(filters.command("getthumbnail", COMMAND_HAND_LER) & sudo_filter)
async def get_thumb_nail(client, message):
    status_message = await message.reply_text("...")
    if message.reply_to_message is not None:
        """reply_to_message = message.reply_to_message
        thumb_image_file_id = None
        file_di_ref = None
        if reply_to_message.document is not None:
            thumb_image_file_id = reply_to_message.document.thumbs[0].file_id
            file_di_ref = reply_to_message.document.file_ref
        if reply_to_message.video is not None:
            thumb_image_file_id = reply_to_message.video.thumbs[0].file_id
            file_di_ref = reply_to_message.video.file_ref
        if thumb_image_file_id is not None:
            print(thumb_image_file_id)
            print(file_di_ref)
            download_location = TMP_DOWNLOAD_DIRECTORY + "/"
            c_time = time.time()
            downloaded_file_name = await client.download_media(
                message=thumb_image_file_id,
                file_ref=file_di_ref,
                file_name=download_location,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to download", message, c_time
                )
            )
            print(downloaded_file_name)
            await client.send_document(
                chat_id=message.chat.id,
                document=downloaded_file_name,
                disable_notification=True,
                reply_to_message_id=message.message_id
            )
            os.remove(downloaded_file_name)
        await message.delete()"""
        await status_message.edit("issues")
    elif os.path.exists(thumb_image_path):
        caption_str = (
            "Currently Saved Thumbnail. " "Clear with <code>.clearthumbnail</code>"
        )
        await message.reply_document(
            document=thumb_image_path, caption=caption_str, disable_notification=True
        )
        await status_message.delete()
    else:
        await status_message.edit(
            "Reply <code>.gethumbnail</code> as a reply to a media"
        )
