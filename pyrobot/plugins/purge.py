"""Purge Messages
Syntax: .purge"""

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER


@Client.on_message(Filters.command("purge", COMMAND_HAND_LER)  & Filters.me)
async def purge(client, message):
    if message.reply_to_message:
        recvd_commands = message.text.split(" ")
        from_user = None
        if len(recvd_commands) > 1:
            user_id = recvd_commands[1]
            from_user = await client.get_users(user_id)
        list_of_messages = await client.get_history(
            chat_id=message.chat.id,
            offset=message.reply_to_message.message_id
        )
        list_of_messages_to_delete = []
        for a_message in list_of_messages:
            if from_user is not None:
                if a_message.from_user == from_user:
                    list_of_messages_to_delete.append(a_message.message_id)
            else:
                list_of_messages_to_delete.append(a_message.message_id)
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=list_of_messages_to_delete,
            revoke=True
        )
    else:
        await message.edit("Reply to a message to purge [user's] messages.")
