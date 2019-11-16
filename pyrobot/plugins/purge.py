"""Purge Messages
Syntax: .purge"""

import asyncio
from datetime import datetime

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER


@Client.on_message(Filters.command("purge", COMMAND_HAND_LER)  & Filters.me)
async def purge(client, message):
    if message.reply_to_message:
        start_t = datetime.now()
        recvd_commands = message.text.split(" ")
        from_user = None
        if len(recvd_commands) > 1:
            user_id = recvd_commands[1]
            from_user = await client.get_users(user_id)
        start_message = message.reply_to_message.message_id
        end_message = message.message_id
        list_of_messages = await client.get_messages(
            chat_id=message.chat.id,
            message_ids=range(start_message, end_message),
            replies=0
        )
        # print(list_of_messages)
        list_of_messages_to_delete = []
        purged_messages_count = 0
        for a_message in list_of_messages:
            if len(list_of_messages_to_delete) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=list_of_messages_to_delete,
                    revoke=True
                )
                purged_messages_count += len(list_of_messages_to_delete)
                list_of_messages_to_delete = []
            if from_user is not None:
                if a_message.from_user == from_user:
                    list_of_messages_to_delete.append(a_message.message_id)
            else:
                list_of_messages_to_delete.append(a_message.message_id)
        print(list_of_messages_to_delete)
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=list_of_messages_to_delete,
            revoke=True
        )
        purged_messages_count += len(list_of_messages_to_delete)
        list_of_messages_to_delete = []
        end_t = datetime.now()
        time_taken_s = (end_t - start_t).seconds
        await message.edit(
            f"<u>purged</u> {purged_messages_count} messages in {time_taken_s} seconds."
        )
        await asyncio.sleep(5)
        await message.delete()
    else:
        await message.edit("Reply to a message to purge [user's] messages.")
