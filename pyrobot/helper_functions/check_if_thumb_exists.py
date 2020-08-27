#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K


import os
import random
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrobot import TMP_DOWNLOAD_DIRECTORY
from pyrobot.helper_functions.run_shell_cmnd import run_command


async def is_thumb_image_exists(file_name: str):
    thumb_image_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
    if os.path.exists(thumb_image_path):
        thumb_image_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
    elif file_name is not None and file_name.lower().endswith(("mp4", "mkv", "webm")):
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        # get a random TTL from the duration
        ttl = str(random.randint(0, duration - 1))
        #
        thumb_image_path = gen_tg_thumbnail(await take_screen_shot(file_name, ttl))
    else:
        thumb_image_path = None
    return thumb_image_path


async def take_screen_shot(file_name: str, ttl: str) -> str:
    out_put_file_name = os.path.join(
        os.path.dirname(file_name),
        ttl + "_" + str(time.time()) + ".jpg"
    )
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        ttl,
        "-i",
        file_name,
        "-vframes",
        "1",
        out_put_file_name
    ]
    stdout, stderr = await run_command(file_genertor_command)
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None


def gen_tg_thumbnail(downloaded_file_name: str) -> str:
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
    img.save(downloaded_file_name, "JPEG")
    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
    return downloaded_file_name
