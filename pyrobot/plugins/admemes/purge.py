"""Purge Messages
Syntax: .purge"""

import asyncio

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER

from pyrobot.helper_functions.admin_check import admin_check


@Client.on_message(Filters.command("purge", COMMAND_HAND_LER))
async def purge(client, message):
    """ purge upto the replied message """
    is_admin = await admin_check(message)

    if not is_admin:
        return

    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []

    if message.reply_to_message:
        message_ids = list(range(
            message.reply_to_message.message_id,
            message.message_id
        ))
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=message_ids,
            revoke=True
        )

    await status_message.edit_text(
        f"deleted {len(message_ids)} messages"
    )
    await asyncio.sleep(5)
    await status_message.delete()
