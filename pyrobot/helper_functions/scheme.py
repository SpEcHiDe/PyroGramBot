"""The entire code is copied without permission
from https://github.com/Lonami/TelethonianBotExt/blob/master/layer.py
modified to suit the needs of this application"""

import asyncio
import io
import sys
from pyrogram import filters
from pyrobot import (
    LAYER_FEED_CHAT,
    LAYER_UPDATE_INTERVAL,
    LAYER_UPDATE_MESSAGE_CAPTION
)
from pyrobot.pyrobot import PyroBot


async def fetch():
    BASE_URI = b"raw.githubusercontent.com"
    URI = b"telegramdesktop/tdesktop/dev/Telegram/Resources/tl/api.tl"
    # We could use aiohttp but this is more fun
    rd, wr = await asyncio.open_connection(BASE_URI, 443, ssl=True)

    # Send HTTP request
    wr.write(
        b"GET /" + URI + b" HTTP/1.1\r\n"
        b"Host: " + BASE_URI + "\r\n"
        b"\r\n"
    )
    await wr.drain()

    # Get response headers
    headers = await rd.readuntil(b"\r\n\r\n")
    if headers[-4:] != b"\r\n\r\n":
        raise ConnectionError("Connection closed")

    # Ensure it"s OK
    if not headers.startswith(b"HTTP/1.1 200 OK"):
        raise ValueError("Bad status code: {}".format(headers[:headers.index(b"\r\n")]))

    # Figure out Content-Length to read
    index = headers.index(b"Content-Length:") + 16
    length = int(headers[index:headers.index(b"\r", index)])
    result = await rd.readexactly(length)

    # Properly close the writer
    wr.close()
    if sys.version_info >= (3, 7):
        await wr.wait_closed()

    return result


async def check_feed(client: PyroBot):
    last_hash = hash(await fetch())
    while True:
        contents = await fetch()
        if hash(contents) != last_hash:
            file = io.BytesIO(contents)
            file.name = "scheme.tl"
            message = await client.send_document(
                LAYER_FEED_CHAT,
                file,
                caption=LAYER_UPDATE_MESSAGE_CAPTION
            )
            await message.pin(disable_notification=True)
            last_hash = hash(contents)
        await asyncio.sleep(LAYER_UPDATE_INTERVAL)
