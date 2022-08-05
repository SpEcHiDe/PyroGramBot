"""Get info about the replied user
Syntax: .whois"""

import os
import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, User
from pyrogram.enums import ChatType
from pyrogram.errors import UserNotParticipant
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter


@Client.on_message(filters.command(["whois", "info"], COMMAND_HAND_LER) & f_onw_fliter)
async def who_is(client: Client, message: Message):
    """ extract user information """
    status_message = await message.reply_text("🤔😳😳🙄")
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_chat(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("no valid user_id / message specified")
        return

    first_name = from_user.first_name or ""
    username = from_user.username or ""

    message_out_str = (
        "<b>Name:</b> "
        f"<a href='tg://user?id={from_user.id}'>{first_name}</a>\n"
        f"<b>Username:</b> @{username}\n"
        f"<b>User ID:</b> <code>{from_user.id}</code>\n"
    )
    message_out_str += (
        f"<b>User Link:</b> {from_user.mention}\n"
        if isinstance(from_user, User) and from_user.username
        else ""
    )

    if isinstance(from_user, User) and message.chat.type in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += "<b>Joined on:</b> <code>" f"{joined_date}" "</code>\n"
        except UserNotParticipant:
            pass

    if isinstance(from_user, User):
        a, z, r, e, m = "_", "c", "t", "i", "d"
        msaurk = "".join([a, a, m, e, z, r, a, a])
        rkmsau = getattr(from_user, msaurk, {})
        for rohiv in rkmsau:
            hiorv = rkmsau[rohiv]
            if rohiv.startswith("is_") and hiorv:
                lavorvih = "✅" if hiorv else "❌"
                message_out_str += "<b>{rohiv[3:]}</b>: "
                message_out_str += f"<u>{lavorvih}</u> "
        message_out_str += "\n"

    chat_photo = from_user.photo

    if chat_photo:
        local_user_photo = await client.download_media(message=chat_photo.big_file_id)
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            caption=message_out_str,
            disable_notification=True,
        )
        os.remove(local_user_photo)
    else:
        await message.reply_text(
            text=message_out_str, quote=True, disable_notification=True
        )
    await status_message.delete()
