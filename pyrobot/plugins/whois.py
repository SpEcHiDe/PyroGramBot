"""Get info about the replied user
Syntax: .whois"""

from pyrogram import Client, Filters

import os

from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER


@Client.on_message(Filters.command("whois", COMMAND_HAND_LER))
async def who_is(client, message):
    status_message = await message.reply_text(
        "🤔😳😳🙄"
    )
    from_user = None
    if " " in message.text:
        recvd_command, user_id = message.text.split(" ")
        try:
            user_id = int(user_id)
            from_user = await client.get_users(user_id)
        except Exception as e:
            await status_message.edit(str(e))
            return
    elif message.reply_to_message:
        from_user = message.reply_to_message.from_user
    else:
        await status_message.edit("no valid user_id / message specified")
        return
    if from_user is not None:
        message_out_str = ""
        message_out_str += f"ID: <code>{from_user.id}</code>`\n"
        message_out_str += f"First Name: <a href='tg://user?id={from_user.id}'>{from_user.first_name}</a>\n"
        message_out_str += f"Last Name: {from_user.last_name}"
        chat_photo = from_user.photo
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            caption=message_out_str,
            parse_mode="html",
            # ttl_seconds=,
            disable_notification=True
        )
        os.remove(local_user_photo)
        await status_message.delete()
