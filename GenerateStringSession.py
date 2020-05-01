#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
from pyrogram import Client


try:
    from pyrobot import APP_ID, API_HASH
except ModuleNotFoundError:
    APP_ID = int(input("enter Telegram APP ID: "))
    API_HASH = input("enter Telegram API HASH: ")


async def main(api_id, api_hash):
    """ generate StringSession for the current MemorySession"""
    async with Client(
            ":memory:",
            api_id=api_id,
            api_hash=api_hash
    ) as app:
        print(app.export_session_string())


if __name__ == "__main__":
    # Then we need a loop to work with
    loop = asyncio.get_event_loop()
    # Then, we need to run the loop with a task
    loop.run_until_complete(main(APP_ID, API_HASH))
