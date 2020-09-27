import json
from pyrogram import filters
from pyrogram.types import (
    Message
)
from pyrobot import (
    COMMAND_HAND_LER,
    WARN_SETTINGS_ID
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.cust_p_filters import (
    sudo_filter
)


@PyroBot.on_message(
    filters.command(["warnlimit", "setwarn"], COMMAND_HAND_LER) &
    sudo_filter
)
async def set_warn_mode_and_limit(client: PyroBot, msg: Message):
    if len(msg.command) <= 1:
        await msg.reply("Input not found!")
        return
    chat_id = str(msg.chat.id)
    WARN_MODE = "kick"
    WARN_LIMIT = 5
    _, args = msg.text.split(maxsplit=1)
    if "ban" in args.lower():
        WARN_MODE = "ban"
        await msg.reply("Warning Mode Updated to <u>Ban</u>")
    elif "kick" in args.lower():
        WARN_MODE = "kick"
        await msg.reply("Warning Mode Updated to <u>Kick</u>")
    elif "mute" in args.lower():
        WARN_MODE = "mute"
        await msg.reply("Warning Mode Updated to <u>Mute</u>")
    elif args.isnumeric():
        input_ = int(args)
        WARN_LIMIT = input_
        await msg.reply(f"Warn limit Updated to <u>{input_}</u> Warns.")
    else:
        await msg.reply("Invalid arguments, Exiting...")
    client.warnsettingsstore[chat_id] = {
        "WARN_LIMIT": WARN_LIMIT,
        "WARN_MODE": WARN_MODE
    }
    await client.save_public_store(
        WARN_SETTINGS_ID,
        json.dumps(client.warnsettingsstore)
    )
