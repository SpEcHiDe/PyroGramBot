"""Execute GNU/Linux commands inside Telegram
Syntax: .exec Code"""
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import asyncio
from io import BytesIO
from pyrogram import Client, filters
from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter


@Client.on_message(filters.command("exec", COMMAND_HAND_LER) & sudo_filter)
async def execution(_, message):
    status_message = await message.reply_text("Processing ...")
    # DELAY_BETWEEN_EDITS = 0.3
    # PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    # start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "😂"
    o = stdout.decode()
    if not o:
        o = "😐"

    OUTPUT = ""
    OUTPUT += f"<b>QUERY:</b>\n<u>Command:</u>\n<code>{cmd}</code> \n"
    OUTPUT += f"<u>PID</u>: <code>{process.pid}</code>\n\n"
    OUTPUT += f"<b>stderr</b>: \n<code>{e}</code>\n\n"
    OUTPUT += f"<b>stdout</b>: \n<code>{o}</code>"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd,
                disable_notification=True
            )
    else:
        await reply_to_.reply_text(OUTPUT)

    await status_message.delete()
