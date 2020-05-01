"""Execute GNU/Linux commands inside Telegram
Syntax: .exec Code"""
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pyrogram import Client, Filters

import asyncio
import os
import time

from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter


@Client.on_message(Filters.command("exec", COMMAND_HAND_LER)  & sudo_filter)
async def execution(client, message):
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "<b>Tip</b>: \n<code>If you want to see the results of your code, I suggest printing them to stdout.</code>"
    
    OUTPUT = f"<b>QUERY:</b>\n<u>Command:</u>\n<code>{cmd}</code> \n<u>PID</u>: <code>{process.pid}</code>\n\n<b>stderr</b>: \n<code>{e}</code>\n\n<b>stdout</b>: \n<code>{o}</code>"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await message.reply_document(
            chat_id=message.chat.id,
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("exec.text")
    else:
        await message.reply_text(OUTPUT)
