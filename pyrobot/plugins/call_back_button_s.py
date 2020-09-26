#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    CallbackQuery
)
from pyrobot import (
    LOGGER
)
from pyrobot.helper_functions.you_tube_dl_button import youtube_dl_call_back


@Client.on_callback_query()
async def button(client, callback_query: CallbackQuery):
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differnetly
    # (and we can only answer once),
    # so we do always answer here.
    # and, do any heavy processing later!
    cb_data = callback_query.data

    if cb_data.startswith("ytdl_"):
        await callback_query.answer(
            text="please wait, the message will be edited after a SHORT time",
            show_alert=False
        )
        _, call_back_data = cb_data.split("_")
        await youtube_dl_call_back(client, callback_query, call_back_data)
