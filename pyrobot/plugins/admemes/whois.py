"""Get info about the replied user
Syntax: .whois"""

from io import BytesIO
from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, User, Chat
from pyrogram.enums import ChatType
from pyrogram.errors import UserNotParticipant
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.file_id import FileId, FileType, ThumbnailSource
from pyrogram.errors import (
    PeerIdInvalid,
    ChannelInvalid,
    UserIdInvalid,
    UsernameNotOccupied
)


@Client.on_message(filters.command(["whois", "info"], COMMAND_HAND_LER) & f_onw_fliter)
async def who_is(client: Client, message: Message):
    """ extract user information """
    status_message = await message.reply_text("🤔😳😳🙄")
    from_user = None
    from_user_id, _, thengaa = extract_user(message)

    small_user = None
    full_user = None
    profile_vid = None

    if thengaa or isinstance(thengaa, User):
        try:
            from_user = await client.invoke(
                GetFullUser(
                    id=(
                        await client.resolve_peer(
                            from_user_id
                        )
                    )
                )
            )
        except UserIdInvalid:
            pass
        except PeerIdInvalid as error:
            return await status_message.edit(str(error))

        if from_user:
            small_user = from_user.users[0]
            full_user = from_user.full_user
            from_user = User._parse(client, small_user)

    if (
        not from_user and
        thengaa or isinstance(thengaa, Chat)
    ):
        try:
            from_user = await client.invoke(
                GetFullChannel(
                    channel=(
                        await client.resolve_peer(
                            from_user_id
                        )
                    )
                )
            )
        except (ChannelInvalid, UsernameNotOccupied) as error:
            return await status_message.edit(str(error))

        small_user = from_user.chats[0]
        full_user = from_user.full_chat
        from_user = Chat._parse_channel_chat(client, small_user)

    if not from_user and thengaa == True:
        return await status_message.edit("🏃🏻‍♂️🏃🏻‍♂️🏃🏻‍♂️")

    first_name = getattr(
        from_user,
        "title",
        getattr(
            from_user,
            "first_name",
            " "
        )
    )
    last_name = getattr(from_user, "last_name", "")
    username = from_user.username or ""

    message_out_str = ""

    if isinstance(from_user, User):
        message_out_str += (
            "<b>Name:</b> "
            f"<a href='tg://user?id={from_user.id}'>{first_name}</a>"
        )

    if isinstance(from_user, Chat):
        puzhu = message.reply_to_message or message
        message_out_str += (
            "<b>Name:</b> "
            f"<a href='{puzhu.link}'>{first_name}</a>"
        )

    if last_name:
        message_out_str += f" <b>{last_name}</b>"
    message_out_str += "\n"

    if getattr(full_user, "private_forward_name", None):
        message_out_str += (
            f"<b>#Tg_Name:</b> <u>{full_user.private_forward_name}</u>\n"
        )

    if username:
        message_out_str += (
            f"<b>Username:</b> @{username}\n"
        )

    message_out_str += (
        f"<b>{type(from_user)} ID:</b> <code>{from_user.id}</code>\n"
    )

    if getattr(full_user, "about", None):
        message_out_str += (
            f"<b>About:</b> <code>{full_user.about}</code>\n"
        )

    if getattr(full_user, "common_chats_count", None):
        message_out_str += (
            f"<b>Groups in Common:</b> <u>{full_user.common_chats_count}</u>\n"
        )

    if (
        isinstance(from_user, User) and
        message.chat.type in [ChatType.SUPERGROUP, ChatType.CHANNEL]
    ):
        try:
            chat_member_p = await message.chat.get_member(small_user.id)
            joined_date = (chat_member_p.joined_date or datetime.fromtimestamp(
                time()
            )).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += "<b>Joined on:</b> <code>" f"{joined_date}" "</code>\n"
        except UserNotParticipant:
            pass

    a, z, r, e, m = "_", "c", "t", "i", "d"
    msaurk = "".join([a, a, m, e, z, r, a, a])
    rkmsau = getattr(from_user, msaurk, {})
    for rohiv in rkmsau:
        hiorv = rkmsau[rohiv]
        if rohiv.startswith("is_") and hiorv:
            lavorvih = "✅" if hiorv else "❌"
            message_out_str += f"<b>{rohiv[3:]}</b>: "
            message_out_str += f"<u>{lavorvih}</u> "
    message_out_str += "\n"

    if len(message_out_str) < 334:
        plose = getattr(
            full_user,
            "settings",
            getattr(
                full_user,
                "available_reactions",
                None
            )
        )
        if plose:
            message_out_str += f"<code>{plose}</code>\n"

    if getattr(full_user, "online_count", None):
        message_out_str += (
            f"<b>online count:</b> <code>{full_user.online_count}</code>\n"
        )

    if getattr(full_user, "pinned_msg_id", None):
        message_out_str += (
            f"<a href='https://t.me/c/{full_user.id}/{full_user.pinned_msg_id}'>"
            "pinned msg"
            "</a>\n"
        )

    if getattr(full_user, "linked_chat_id", None):
        message_out_str += (
            f"<a href='https://t.me/c/{full_user.linked_chat_id}/1'>"
            "linked chat"
            "</a>\n"
        )

    chat_photo = from_user.photo

    if chat_photo:
        p_p_u_t = None
        tUpo = getattr(
            full_user,
            "profile_photo",
            getattr(
                full_user,
                "chat_photo",
                None
            )
        )
        if tUpo:
            profile_vid = tUpo.video_sizes[0] if tUpo.video_sizes else None
            p_p_u_t = datetime.fromtimestamp(
                tUpo.date
            ).strftime(
                "%Y.%m.%d %H:%M:%S"
            )
        if p_p_u_t:
            message_out_str += f"<b>Upload Date</b>: <u>{p_p_u_t}</u>\n"
        if profile_vid:
            file_obj = BytesIO()
            async for chunk in client.stream_media(
                message=FileId(
                    file_type=FileType.PHOTO,
                    dc_id=tUpo.dc_id,
                    media_id=tUpo.id,
                    access_hash=tUpo.access_hash,
                    file_reference=tUpo.file_reference,
                    thumbnail_source=ThumbnailSource.THUMBNAIL,
                    thumbnail_file_type=FileType.PHOTO,
                    thumbnail_size=profile_vid.type,
                    volume_id=0,
                    local_id=0,
                ).encode(),
            ):
                file_obj.write(chunk)
            file_obj.name = "profile_vid_.mp4"
            await message.reply_video(
                video=file_obj,
                quote=True,
                caption=message_out_str,
                disable_notification=True,
            )
        else:
            file_obj = BytesIO()
            async for chunk in client.stream_media(
                message=chat_photo.big_file_id,
            ):
                file_obj.write(chunk)
            file_obj.name = "profile_pic_.jpg"
            await message.reply_photo(
                photo=file_obj,
                quote=True,
                caption=message_out_str,
                disable_notification=True,
            )
    else:
        await message.reply_text(
            text=message_out_str, quote=True, disable_notification=True
        )

    await status_message.delete()
