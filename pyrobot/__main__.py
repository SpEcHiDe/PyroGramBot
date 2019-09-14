#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os

# the secret configuration specific things
if bool(os.environ.get("ENV", False)):
    from .sample_config import Config
else:
    from .config import Config


if __name__ == "__main__":
    plugins = dict(
        root="./plugins"
    )
    app = pyrogram.Client(
        Config.HU_STRING_SESSION,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    app.run()
