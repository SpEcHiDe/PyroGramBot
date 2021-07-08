#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# needed to appropriately, select ENV vars / Config vars
import os

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


from pyrobot.sample_config import Config


# TODO: is there a better way?
LOGGER = logging.getLogger(__name__)
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
TG_COMPANION_BOT = Config.TG_COMPANION_BOT
COMMAND_HAND_LER = Config.COMMAND_HAND_LER
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
# create download directory, if not exist
if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(TMP_DOWNLOAD_DIRECTORY)
HEROKU_API_KEY = Config.HEROKU_API_KEY
OFFICIAL_UPSTREAM_REPO = Config.OFFICIAL_UPSTREAM_REPO
DB_URI = Config.DB_URI
TG_URI = int(Config.TG_URI)
G_DRIVE_CLIENT_ID = Config.G_DRIVE_CLIENT_ID
G_DRIVE_CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
IS_BOT = True
USE_AS_BOT = True
OWNER_ID = Config.OWNER_ID
SUDO_USERS = list(Config.SUDO_USERS)
SUDO_USERS.append(OWNER_ID)
SUDO_USERS = list(set(SUDO_USERS))
TG_MAX_SELECT_LEN = int(Config.TG_MAX_SELECT_LEN)
TG_IRU_S_M_ID = int(Config.TG_IRU_S_M_ID)
WARN_DATA_ID = int(Config.WARN_DATA_ID)
WARN_SETTINGS_ID = int(Config.WARN_SETTINGS_ID)
# define the "types" that should be uplaoded as streamable
# copied from SpEcHiDe/UniBorg
TL_VID_STREAM_TYPES = ("MP4", "WEBM", "MKV")
TL_MUS_STREAM_TYPES = ("MP3", "WAV", "FLAC")
TL_FF_NOAQ_TYPES = ("WEBP")
A_PIN_MESSAGE_ID = int(Config.A_PIN_MESSAGE_ID)
LAYER_FEED_CHAT = Config.LAYER_FEED_CHAT
if LAYER_FEED_CHAT:
    LAYER_FEED_CHAT = int(LAYER_FEED_CHAT)
LAYER_UPDATE_INTERVAL = Config.LAYER_UPDATE_INTERVAL
if LAYER_UPDATE_INTERVAL:
    LAYER_UPDATE_INTERVAL = int(LAYER_UPDATE_INTERVAL)
LAYER_UPDATE_MESSAGE_CAPTION = Config.LAYER_UPDATE_MESSAGE_CAPTION
