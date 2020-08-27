# Copyright (C) 2020 by SpEcHiDe@Github, < https://github.com/SpEcHiDe >.
#
# This file is part of < https://github.com/SpEcHiDe/PyroGramBot > project,
# and is released under the "GNU Affero General Public License v3.0 License Agreement".
# Please see < https://github.com/SpEcHiDe/PyroGramBot/raw/master/COPYING >
#
"""IX.IO pastebin like site
Syntax: .paste"""

import aiohttp
import json
import os
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrobot import (
    COMMAND_HAND_LER,
    TMP_DOWNLOAD_DIRECTORY
)


@Client.on_message(filters.command("paste", COMMAND_HAND_LER))
async def paste_bin(_, message):
    status_message = await message.reply_text("...")
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
        "deldog": "https://del.dog/documents",
        "nekobin": "https://nekobin.com/api/documents"
    }

    chosen_store = "nekobin"
    if len(message.command) == 2:
        chosen_store = message.command[1]
    
    # get the required pastebin URI
    paste_store_url = paste_bin_store_s.get(chosen_store, paste_bin_store_s["nekobin"])
    paste_store_base_url_rp = urlparse(paste_store_url)

    # the pastebin sites, respond with only the "key"
    # we need to prepend the BASE_URL of the appropriate site
    paste_store_base_url = paste_store_base_url_rp.scheme + "://" + \
        paste_store_base_url_rp.netloc
    
    async with aiohttp.ClientSession() as session:
        response_d = await session.post(paste_store_url, json=json_paste_data)
        response_jn = await response_d.json()
    
    # we got the response from a specific site,
    # this dictionary needs to be scrapped
    # using bleck megick to find the "key"
    t_w_attempt = bleck_megick(response_jn)
    required_url = json.dumps(t_w_attempt, sort_keys=True, indent=4) + "\n\n #ERROR"
    if t_w_attempt is not None:
        required_url = paste_store_base_url + "/" + "raw" + "/" + t_w_attempt
    
    await status_message.edit(required_url)


def bleck_megick(dict_rspns):
    # first, try getting "key", dirctly
    first_key_r = dict_rspns.get("key")
    # this is for the "del.dog" site
    if first_key_r is not None:
        return first_key_r
    check_if_result_ests = dict_rspns.get("result")
    if check_if_result_ests is not None:
        # this is for the "nekobin.com" site
        second_key_a = check_if_result_ests.get("key")
        if second_key_a is not None:
            return second_key_a
    # TODO: is there a better way?
    return None
