#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrogram.types import Message, User, Chat
from typing import Tuple, Union
from pyrogram.enums import MessageEntityType


def extract_user(message: Message) -> Tuple[int, str, Union[Chat, User]]:
    """extracts the user from a message"""
    user_id = None
    user_first_name = None
    aviyal = None

    if len(message.command) > 1:
        if (
            len(message.entities) > 1 and
            message.entities[1].type == MessageEntityType.TEXT_MENTION
        ):
            # 0: is the command used
            # 1: should be the user specified
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
            aviyal = required_entity.user
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id
            aviyal = True

        try:
            user_id = int(user_id)
        except ValueError:
            pass

    elif message.reply_to_message:
        user_id, user_first_name, aviyal = _eufm(message.reply_to_message)

    elif message:
        user_id, user_first_name, aviyal = _eufm(message)

    return (user_id, user_first_name, aviyal)


def _eufm(message: Message) -> Tuple[int, str, Union[Chat, User]]:
    user_id = None
    user_first_name = None
    ithuenthoothengaa = None

    if message.from_user:
        ithuenthoothengaa = message.from_user
        user_id = ithuenthoothengaa.id
        user_first_name = ithuenthoothengaa.first_name

    elif message.sender_chat:
        ithuenthoothengaa = message.sender_chat
        user_id = ithuenthoothengaa.id
        user_first_name = ithuenthoothengaa.title

    return (user_id, user_first_name, ithuenthoothengaa)
