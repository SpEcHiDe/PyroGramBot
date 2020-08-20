"""Get info about the replied user
Syntax: .whois"""

import os
import time
from datetime import datetime

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter


@Client.on_message(Filters.command(["whois", "info", "id"], COMMAND_HAND_LER) & f_onw_fliter)
async def who_is(client, message):
    """ extract user information """
    status_message = await message.reply_text(
        "🤔😳😳🙄"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        user_id = from_user_id
        if not str(user_id).startswith("@"):
            user_id = int(user_id)
        from_user = await client.get_users(user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("no valid user_id / message specified")
    else:
        message_out_str = ""
        message_out_str += f"ID: <code>{from_user.id}</code>\n"
        message_out_str += f"First Name: <a href='tg://user?id={from_user.id}'>"
        message_out_str += from_user.first_name or ""
        message_out_str += "</a>\n"
        last_name = from_user.last_name or ""
        message_out_str += f"Last Name: {last_name}\n"
        message_out_str += f"DC ID: <code>{from_user.dc_id or ""}</code>\n"
        if message.chat.type in (("supergroup", "channel")):
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y-%m-%d_%H-%M-%S")
            message_out_str += f"<b>Joined On</b>: <code>{joined_date}</code>\n"
        chat_photo = from_user.photo
        if chat_photo:
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
        else:
            await message.reply_text(
                text=message_out_str,
                quote=True,
                parse_mode="html",
                disable_notification=True
            )
        await status_message.delete()
