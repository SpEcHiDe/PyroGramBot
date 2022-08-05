#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrogram.types import Message
from typing import Tuple
from pyrogram.enums import MessageEntityType


def extract_user(message: Message) -> Tuple[int, str]:
    """extracts the user from a message"""
    user_id = None
    user_first_name = None

    if len(message.command) > 1:
        if len(message.entities) > 1 and message.entities[1].type == MessageEntityType.TEXT_MENTION:
            # 0: is the command used
            # 1: should be the user specified
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id

        try:
            user_id = int(user_id)
        except ValueError:
            print("പൊട്ടൻ ")

    elif message.reply_to_message:
        user_id, user_first_name = _eufm(message.reply_to_message)

    elif message:
        user_id, user_first_name = _eufm(message)

    return (user_id, user_first_name)


def _eufm(message: Message) -> Tuple[int, str]:
    user_id = None
    user_first_name = None

    if message.from_user:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name

    elif message.sender_chat:
        user_id = message.sender_chat.id
        user_first_name = message.sender_chat.title

    return (user_id, user_first_name)
