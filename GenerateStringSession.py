#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


import asyncio
import os

try:
    from pyrobot import APP_ID, API_HASH
except ModuleNotFoundError:
    APP_ID = int(input("enter Telegram APP ID: "))
    API_HASH = input("enter Telegram API HASH: "))


import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def main(APP_ID, API_HASH):
    async with pyrogram.Client(
        ":memory:",
        api_id=APP_ID,
        api_hash=API_HASH
    ) as app:
        print(app.export_session_string())


if __name__ == "__main__":
    # Then we need a loop to work with
    loop = asyncio.get_event_loop()
    # Then, we need to run the loop with a task
    loop.run_until_complete(main(APP_ID, API_HASH))
