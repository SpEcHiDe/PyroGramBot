from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import (
    admin_fliter
)

@Client.on_message(
    filters.command(["pin"], COMMAND_HAND_LER) &
    admin_fliter
)
async def pin(client, message):
    await client.pin_chat_message(
    message.chat.id,
    message.reply_to_message.message_id
    )

@Client.on_message(
    filters.command(["unpin"], COMMAND_HAND_LER) &
    admin_fliter
)
async def unpin(client, message):
    await client.unpin_chat_message(
    message.chat.id,
    message.reply_to_message.message_id
    )

@Client.on_message(
    filters.command(["unpinall"], COMMAND_HAND_LER) &
    admin_fliter
)
async def unpinall(client, message):
    await client.unpin_all_chat_messages(
        message.chat.id
    )
