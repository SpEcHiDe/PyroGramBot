"""Purge Messages
Syntax: .purge"""

import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrobot import COMMAND_HAND_LER, TG_MAX_SELECT_LEN
from pyrobot.helper_functions.cust_p_filters import admin_fliter


@Client.on_message(filters.command("purge", COMMAND_HAND_LER) & admin_fliter)
async def purge(client, message):
    """ purge upto the replied message """
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        # https://t.me/c/1312712379/84174
        return

    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.id, message.id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == TG_MAX_SELECT_LEN:
                count_del_etion_s += await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                message_ids = []
        if len(message_ids) > 0:
            count_del_etion_s += await client.delete_messages(
                chat_id=message.chat.id, message_ids=message_ids, revoke=True
            )

    await status_message.edit_text(f"deleted {count_del_etion_s} messages")
    await asyncio.sleep(5)
    await status_message.delete()
