#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)


from pyrobot import (
    HU_STRING_SESSION,
    TG_COMPANION_BOT,
    APP_ID, 
    API_HASH, 
    DB_URI,
    IS_BOT
)    

import asyncio
import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def main():
    # exclude_plugins = []
    # if DB_URI is not None:
    #     exclude_plugins = ["dbplugins"]
    plugins = dict(
        root="pyrobot/plugins",
        # exclude=exclude_plugins
    )
    
    if HU_STRING_SESSION is None:
    	app = pyrogram.Client(
            "TG_COMPANION_BOT",
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_COMPANION_BOT,
            plugins=plugins
        )
    else:
    	app = pyrogram.Client(
            HU_STRING_SESSION,
            api_id=APP_ID,
            api_hash=API_HASH,
            plugins=plugins
        )
        
    #
    app.run()
    
    
if __name__ == "__main__":
	main()