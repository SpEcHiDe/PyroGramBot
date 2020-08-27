"""Telegram Ping / Pong Speed
Syntax: .ping"""

import time
from pyrogram import Client, filters
from pyrobot import (
    COMMAND_HAND_LER,
    IS_BOT
)

# -- Constants -- #
ALIVE = "ചത്തിട്ടില്ലാ..."
HELP = "CAADAgAD6AkAAowucAABsFGHedLEzeUWBA"
REPO = ("User / Bot is available on GitHub:\n"
        "https://github.com/SpEcHiDe/PyroGramBot")
# -- Constants End -- #


@Client.on_message(filters.command(["alive", "start"], COMMAND_HAND_LER))
async def check_alive(_, message):
    await message.reply_text(ALIVE)


@Client.on_message(filters.command("help", COMMAND_HAND_LER))
async def help_me(_, message):
    await message.reply_sticker(HELP)


@Client.on_message(filters.command("ping", COMMAND_HAND_LER))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")


@Client.on_message(filters.command("repo", COMMAND_HAND_LER))
async def repo(_, message):
    await message.reply_text(REPO)
