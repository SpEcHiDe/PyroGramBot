"""Telegram Ping / Pong Speed
Syntax: .ping"""

from pyrogram import Client, Filters

from datetime import datetime

from pyrobot import COMMAND_HAND_LER


@Client.on_message(Filters.command("ping", COMMAND_HAND_LER)  & Filters.me)
async def jsonify(client, message):
    start_t = datetime.now()
    await message.edit("Pong!")
    end_t = datetime.now()
    time_taken_s = (end_t - start_t).microseconds / 1000
    await message.edit(f"Ping Pong Speed\n{time_taken_s} milli-seconds")
