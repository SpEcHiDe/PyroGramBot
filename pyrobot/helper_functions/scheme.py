"""The entire code is copied without permission
from https://github.com/Lonami/TelethonianBotExt/blob/master/layer.py
modified to suit the needs of this application"""

import asyncio
import aiohttp
import os
from io import BytesIO
from pyrogram import filters
from pyrobot import LAYER_FEED_CHAT, LAYER_UPDATE_INTERVAL, LAYER_UPDATE_MESSAGE_CAPTION


async def fetch(scheme_url: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(scheme_url)
        return str.encode(await response.text())


async def check_feed(client):
    layer_uri = (
        "https://"
        "github.com"
        "/telegramdesktop/tdesktop/raw/dev/Telegram/Resources/tl/"
        "api.tl"
    )
    last_hash = hash(await fetch(layer_uri))
    while True:
        contents = await fetch(layer_uri)
        if hash(contents) != last_hash:
            file = BytesIO(contents)
            file.name = os.path.basename(layer_uri)
            message = await client.send_document(
                LAYER_FEED_CHAT, file, caption=LAYER_UPDATE_MESSAGE_CAPTION
            )
            await message.pin(disable_notification=True)
            last_hash = hash(contents)
        await asyncio.sleep(LAYER_UPDATE_INTERVAL)
