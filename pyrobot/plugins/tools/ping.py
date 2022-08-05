"""Telegram Ping / Pong Speed
Syntax: .ping"""

import time
from pyrogram import Client, filters, __version__
from pyrogram.raw.all import layer
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter

# -- Constants -- #
ALIVE = (
    "ചത്തിട്ടില്ലാ..."
    f"\nL{layer}"
    f"\nv{__version__}"
)
HELP = "CAADAgAD6AkAAowucAABsFGHedLEzeUWBA"
REPO = "User / Bot is available on GitHub:\n" "https://github.com/SpEcHiDe/PyroGramBot"
# -- Constants End -- #


@Client.on_message(filters.command(["alive", "start"], COMMAND_HAND_LER) & f_onw_fliter)
async def check_alive(_, message):
    await message.reply_text(ALIVE)


@Client.on_message(filters.command("help", COMMAND_HAND_LER) & f_onw_fliter)
async def help_me(_, message):
    await message.reply_sticker(HELP)


@Client.on_message(filters.command("ping", COMMAND_HAND_LER) & f_onw_fliter)
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")


@Client.on_message(filters.command("repo", COMMAND_HAND_LER) & f_onw_fliter)
async def repo(_, message):
    await message.reply_text(REPO)
