#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import aiohttp
from json import dumps
from pyrogram.types import CallbackQuery
from pyrobot import paste_bin_store_s
from pyrobot.pyrobot import PyroBot


async def del_pasty_ao(client: PyroBot, c_q: CallbackQuery):
    _, AlbertEinsteinTG_dt, pasty_id = c_q.data.split("_")
    if not c_q.message.reply_to_message:
        await c_q.answer(
            text=("cannot delete, " "if you deleted the original message"),
            show_alert=True,
        )
        return False
    if c_q.from_user.id != c_q.message.reply_to_message.from_user.id:
        await c_q.answer(text=("this is not your paste!!"), show_alert=True)
        return False

    await c_q.answer(text="✅ deleted pasty.lus.pm")

    pasty = paste_bin_store_s.get("pasty")
    # only pasty.lus.pm supports
    # deletion at the moment
    async with aiohttp.ClientSession() as requests:
        AlbertEinsteinTG_url = f"{pasty.get('URL')}/{pasty_id}"
        AlbertEinsteinTG_headers = pasty.get("HEADERS")
        await requests.request(
            method="DELETE",
            url=AlbertEinsteinTG_url,
            data=dumps({"deletionToken": AlbertEinsteinTG_dt}),
            headers=AlbertEinsteinTG_headers,
        )
    await c_q.message.edit_text(
        text=(f"❌ <s>{c_q.message.text}</s>"), reply_markup=None
    )
