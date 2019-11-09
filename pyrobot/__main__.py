#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


from pyrobot import HU_STRING_SESSION, APP_ID, API_HASH, DB_URI

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":
    # exclude_plugins = []
    # if DB_URI is not None:
    #     exclude_plugins = ["dbplugins"]
    plugins = dict(
        root="pyrobot/plugins",
        # exclude=exclude_plugins
    )
    app = pyrogram.Client(
        HU_STRING_SESSION,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    #
    app.run()
