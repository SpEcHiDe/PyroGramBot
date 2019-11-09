#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os

# the secret configuration specific things
if bool(os.environ.get("ENV", False)):
    from pyrobot.sample_config import Config
else:
    from pyrobot.config import Development as Config


# TODO: is there a better way?
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
HU_STRING_SESSION = Config.HU_STRING_SESSION
COMMAND_HAND_LER = Config.COMMAND_HAND_LER
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
HEROKU_API_KEY = Config.HEROKU_API_KEY
OFFICIAL_UPSTREAM_REPO = Config.OFFICIAL_UPSTREAM_REPO
DB_URI = Config.DB_URI
G_DRIVE_CLIENT_ID = Config.G_DRIVE_CLIENT_ID
G_DRIVE_CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
