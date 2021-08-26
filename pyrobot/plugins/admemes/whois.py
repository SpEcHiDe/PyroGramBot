"""Get info about the replied user
Syntax: .whois"""

import os
import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter


@Client.on_message(
    filters.command(["whois", "info", "id"], COMMAND_HAND_LER) &
    f_onw_fliter
)
async def who_is(client, message):
    """ extract user information """
    status_message = await message.reply_text(
        "🤔😳😳🙄"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("no valid user_id / message specified")
    message_out_str = ""
        message_out_str += "<b>Name:</b> "
        message_out_str += f"<a href='tg://user?id={from_user.id}'>"
        message_out_str += from_user.first_name or ""
        message_out_str += "</a>\n"
        last_name = from_user.last_name or ""
        message_out_str += f"<b>Suffix:</b> {last_name}\n"
        username = from_user.username or ""
        message_out_str += f"<b>Username:</b> @{username}\n"
        message_out_str += f"<b>User ID:</b> <code>{from_user.id}</code>\n"
        dc_id = from_user.dc_id or "[User Doesnt Have A Valid DP 👀]"
        message_out_str += f"<b>DC ID:</b> <code>{dc_id}</code>\n"
        message_out_str += f"<b>User Link:</b> {from_user.mention}\n" if from_user.username else ""
        message_out_str += f"<b>Is Deleted:</b> True\n" if from_user.is_deleted else ""
        message_out_str += f"<b>Is Verified:</b> True" if from_user.is_verified else ""
        message_out_str += f"<b>Is Scam:</b> True" if from_user.is_scam else ""
        message_out_str += f"<b>Last Seen:</b> <code>{last_online(from_user)}</code>\n\n"
        if message.chat.type in (("supergroup", "channel")):
            try:
                chat_member_p = await message.chat.get_member(from_user.id)
                joined_date = datetime.fromtimestamp(
                    chat_member_p.joined_date or time.time()
                ).strftime("%Y.%m.%d %H:%M:%S")
                message_out_str += (
                    "<b>Joined on:</b> <code>"
                    f"{joined_date}"
                    "</code>\n"
                )
            except UserNotParticipant:
                pass
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

def last_online(from_user):
    time = ""
    if from_user.is_bot:
        time += "🤖 Bot :("
    elif from_user.status == 'recently':
        time += "Recently"
    elif from_user.status == 'within_week':
        time += "Within the last week"
    elif from_user.status == 'within_month':
        time += "Within the last month"
    elif from_user.status == 'long_time_ago':
        time += "A long time ago :("
    elif from_user.status == 'online':
        time += "Currently Online"
    elif from_user.status == 'offline':
        time += datetime.fromtimestamp(from_user.last_online_date).strftime("%a, %d %b %Y, %H:%M:%S")
    return time
