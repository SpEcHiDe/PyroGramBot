#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import json
import os
import time

from pyrobot import TMP_DOWNLOAD_DIRECTORY
from pyrogram import InputMediaDocument


async def load_db(pyro_client, chat_id, message_id):
    db_message = await pyro_client.get_messages(
        chat_id=chat_id,
        message_ids=message_id
    )
    tmp_file_name = os.path.join(
        TMP_DOWNLOAD_DIRECTORY,
        "tmp" + str(time.time()) + "_pyrogram.db"
    )
    downloaded_file_name = await pyro_client.download_media(
        message=db_message,
        file_name=tmp_file_name
    )
    return_val = {}
    if os.path.isfile(downloaded_file_name):
        with open(downloaded_file_name, "r") as fp:
            return_val = json.load(fp)
        os.remove(downloaded_file_name)
    return return_val


async def save_db(pyro_client, chat_id, message_id, db_store):
    tmp_file_name = "pyrogram.db"
    with open(tmp_file_name, "w") as fp:
        json.dump(db_store, fp)
    thumb_image_path = "./pyrobot/helper_functions/Pyrogram.jpg"
    await pyro_client.edit_message_media(
        chat_id=chat_id,
        message_id=message_id,
        media=InputMediaDocument(
            media=tmp_file_name,
            thumb=thumb_image_path,
            caption="pyrogram.db // do not touch",
            parse_mode="html"
        )
    )
    os.remove(tmp_file_name)
