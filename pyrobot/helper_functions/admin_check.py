#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus


async def admin_check(message: Message) -> bool:
    if not message.from_user:
        return False

    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return False

    if message.from_user.id in [
        777000,  # Telegram Service Notifications
        1087968824,  # GroupAnonymousBot
    ]:
        return True

    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
    if check_status.status not in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    ]:
        return False
    else:
        return True
