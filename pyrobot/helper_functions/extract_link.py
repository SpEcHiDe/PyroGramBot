#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

from pyrogram.types import Message, MessageEntity
from pyrogram.enums import MessageEntityType


def extract_url_from_entity(entities: MessageEntity, text: str):
    url = None
    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:
            url = entity.url
        elif entity.type == MessageEntityType.URL:
            o_ = entity.offset
            l_ = entity.length
            url = text[o_ : o_ + l_]
    return url


def extract_link(message: Message):
    custom_file_name = None
    url = None
    youtube_dl_username = None
    youtube_dl_password = None

    if message is None:
        url = None
        custom_file_name = None

    elif message.text is not None:
        if "|" in message.text:
            url_parts = message.text.split("|")
            if len(url_parts) == 2:
                url = url_parts[0]
                custom_file_name = url_parts[1]
            elif len(url_parts) == 4:
                url = url_parts[0]
                custom_file_name = url_parts[1]
                youtube_dl_username = url_parts[2]
                youtube_dl_password = url_parts[3]

        elif message.entities is not None:
            url = extract_url_from_entity(message.entities, message.text)

        else:
            url = message.text.strip()

    elif message.caption is not None:
        if "|" in message.caption:
            url_parts = message.caption.split("|")
            if len(url_parts) == 2:
                url = url_parts[0]
                custom_file_name = url_parts[1]
            elif len(url_parts) == 4:
                url = url_parts[0]
                custom_file_name = url_parts[1]
                youtube_dl_username = url_parts[2]
                youtube_dl_password = url_parts[3]

        elif message.caption_entities is not None:
            url = extract_url_from_entity(message.caption_entities, message.caption)

        else:
            url = message.caption.strip()

    elif message.entities is not None:
        url = message.text

    # trim blank spaces from the URL
    # might have some issues with #45
    if url is not None:
        url = url.strip()
    if custom_file_name is not None:
        custom_file_name = custom_file_name.strip()
    # https://stackoverflow.com/a/761825/4723940
    if youtube_dl_username is not None:
        youtube_dl_username = youtube_dl_username.strip()
    if youtube_dl_password is not None:
        youtube_dl_password = youtube_dl_password.strip()

    return url, custom_file_name, youtube_dl_username, youtube_dl_password
