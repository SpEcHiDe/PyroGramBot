#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

from pyrobot import (
    HU_STRING_SESSION,
    TG_COMPANION_BOT,
    APP_ID, 
    API_HASH, 
    DB_URI,
    LOGGER,
    IS_BOT,
    OWNER_ID,
    SUDO_USERS
)    

from pyrogram import Client, Message
from pyrogram import __version__
from pyrogram.api.all import layer


class PyroGramBot(Client):
    
    def __init__(self):
        name = "pyrobot"

        if HU_STRING_SESSION is None:
            super().__init__(
                name,
                plugins=dict(root=f"{name}/plugins"),  
                workdir=".",      
                api_id=APP_ID,
                api_hash=API_HASH,
                bot_token=TG_COMPANION_BOT
            )
        else:
            super().__init__(
                name,
                plugins=dict(root=f"{name}/plugins"),
                workdir=".",
                api_id=APP_ID,
                api_hash=API_HASH,
            )

    async def start(self):
        await super().start()

        me = await self.get_me()
        IS_BOT = me.is_bot
        LOGGER.info(f"PyroGramBot based on Pyrogram v{__version__} (Layer {layer}) started on @{me.username}. Hi.")


    async def stop(self, *args):
        await super().stop()
        print("PyroGramBot stopped. Bye.")
