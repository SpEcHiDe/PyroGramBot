#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client, __version__
from pyrogram.errors import MessageNotModified
from pyrogram.raw.all import layer
from pyrogram.enums import ParseMode
from pyrobot import (
    APP_ID,
    API_HASH,
    LAYER_UPDATE_INTERVAL,
    LOGGER,
    # OWNER_ID,
    # SUDO_USERS,
    TG_COMPANION_BOT,
    TMP_DOWNLOAD_DIRECTORY,
    TG_URI,
    TG_IRU_S_M_ID,
    WARN_DATA_ID,
    WARN_SETTINGS_ID,
)
from pyrobot.helper_functions.scheme import check_feed
try:
    from pyrobot.a import A
except ImportError:
    pass


class PyroBot(Client):
    filterstore: Dict[str, Dict[str, str]] = defaultdict(dict)
    warndatastore: Dict[str, Dict[str, Union[str, int, List[str]]]] = defaultdict(dict)
    warnsettingsstore: Dict[str, str] = defaultdict(dict)

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            name="PyroGramBot",
            plugins=dict(root=f"{name}/plugins"),
            workdir=TMP_DOWNLOAD_DIRECTORY,
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_COMPANION_BOT,
            parse_mode=ParseMode.HTML,
            sleep_threshold=60,
            # in_memory=True,
            skip_updates=False,
        )

    async def start(self):
        await super().start()
        usr_bot_me = self.me
        self.filterstore = await self.load_public_store(TG_IRU_S_M_ID)
        self.warndatastore = await self.load_public_store(WARN_DATA_ID)
        self.warnsettingsstore = await self.load_public_store(WARN_SETTINGS_ID)
        if LAYER_UPDATE_INTERVAL:
            await check_feed(self)
        LOGGER.info(
            f"PyroGramBot based on Pyrogram v{__version__} "
            f"(Layer {layer}) started on @{usr_bot_me.username}. "
            "Hi."
        )
        try:
            self.B, self.C = await A(self).start()
        except NameError:
            pass


    async def stop(self, *args):
        await self.save_public_store(TG_IRU_S_M_ID, json.dumps(self.filterstore))
        await self.save_public_store(WARN_DATA_ID, json.dumps(self.warndatastore))
        await self.save_public_store(
            WARN_SETTINGS_ID, json.dumps(self.warnsettingsstore)
        )
        await super().stop()
        LOGGER.info("PyroGramBot stopped. Bye.")

    async def load_public_store(self, message_id: int) -> Dict:
        if message_id != 0:
            _check_message = await self.get_messages(
                chat_id=TG_URI, message_ids=message_id, replies=0
            )
            if _check_message:
                return json.loads(_check_message.text)
        return {}

    async def save_public_store(self, message_id: int, text: str):
        if message_id != 0:
            try:
                await self.edit_message_text(
                    chat_id=TG_URI,
                    message_id=message_id,
                    text=f"<code>{text}</code>",
                    disable_web_page_preview=True,
                )
            except MessageNotModified:
                pass
