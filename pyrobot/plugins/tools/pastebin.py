# Copyright (C) 2020 by SpEcHiDe@Github, < https://github.com/SpEcHiDe >.
#
# This file is part of < https://github.com/SpEcHiDe/PyroGramBot > project,
# and is released under the
# "GNU Affero General Public License v3.0 License Agreement".
# Please see < https://github.com/SpEcHiDe/PyroGramBot/raw/master/COPYING >
#
"""IX.IO pastebin like site
Syntax: .paste"""

import aiohttp
from json import loads
from json.decoder import JSONDecodeError
import os
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrobot import (
    COMMAND_HAND_LER,
    TMP_DOWNLOAD_DIRECTORY
)


@Client.on_message(filters.command("paste", COMMAND_HAND_LER))
async def paste_bin(_, message):
    status_message = await message.reply_text(
        "...",
        quote=True
    )
    downloaded_file_name = None

    # first we need to get the data to be pasted
    if message.reply_to_message and message.reply_to_message.media:
        downloaded_file_name_res = await message.reply_to_message.download(
            file_name=TMP_DOWNLOAD_DIRECTORY
        )
        m_list = None
        with open(downloaded_file_name_res, "rb") as fd:
            m_list = fd.readlines()
        downloaded_file_name = ""
        for m in m_list:
            downloaded_file_name += m.decode("UTF-8")
        os.remove(downloaded_file_name_res)
    elif message.reply_to_message:
        downloaded_file_name = message.reply_to_message.text.html
    # elif len(message.command) > 1:
    #     downloaded_file_name = " ".join(message.command[1:])
    else:
        await status_message.edit("എന്ത് ചെയ്യണം എന്ന് പറഞ്ഞില്ല")
        return

    if downloaded_file_name is None:
        await status_message.edit("എന്ത് ചെയ്യണം എന്ന് പറഞ്ഞില്ല")
        return

    json_paste_data = {
        "content": downloaded_file_name
    }

    # a dictionary to store different pastebin URIs
    paste_bin_store_s = {
        # "deldog": {
        #   "URL": "https://del.dog/documents",
        #   "GAS": "https://github.com/dogbin/dogbin",
        # },
        "nekobin": {
            "URL": "https://nekobin.com/api/documents",
            "RAV": "result.key",
            "GAS": "https://github.com/nekobin/nekobin",
        },
        "pasty": {
            "URL": "https://pasty.lus.pm/api/v1/pastes",
            "HEADERS": {
                "User-Agent": "PyroGramBot/6.9",
                "Content-Type": "application/json",
            },
            "RAV": "id",
            "GAS": "https://github.com/lus/pasty",
        },
        "pasting": {
            "URL": "https://pasting.codes/api",
        },
    }

    chosen_store = "nekobin"
    if len(message.command) == 2:
        chosen_store = message.command[1]

    # get the required pastebin URI
    paste_store_ = paste_bin_store_s.get(
        chosen_store
    )

    if not paste_store_:
        av_kys = ", ".join(paste_bin_store_s.keys())
        await status_message.edit(
            f"<b><u>available keys</u></b>: {av_kys}"
        )
        return

    paste_store_url = paste_store_.get("URL")
    paste_store_base_url_rp = urlparse(paste_store_url)

    # the pastebin sites, respond with only the "key"
    # we need to prepend the BASE_URL of the appropriate site
    paste_store_base_url = paste_store_base_url_rp.scheme + \
        "://" + \
        paste_store_base_url_rp.netloc

    async with aiohttp.ClientSession() as session:
        response_d = await session.post(
            paste_store_url,
            json=json_paste_data,
            headers=paste_store_.get("HEADERS")
        )
        response_jn = await response_d.text()
        print(response_jn)
        try:
            response_jn = loads(response_jn.strip())
        except JSONDecodeError:
            # some sites, do not have JSON response
            pass

    rk = paste_store_.get("RAV")
    if rk and "." in rk:
        rkp = rk.split(".")
        for kp in rkp:
            response_jn = response_jn.get(kp)
    elif not rk:
        response_jn = response_jn[1:]
    else:
        response_jn = response_jn.get(rk)
    required_url = paste_store_base_url + "/" + response_jn
    # finally, edit the bot sent message
    await status_message.delete()
    await message.reply_text(
        required_url,
        quote=True
    )
