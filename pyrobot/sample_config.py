#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  GetSongsBot
#  Copyright (C) 2021 The Authors

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from dotenv import load_dotenv


# apparently, no error appears even if the path does not exists
load_dotenv("config.env")


class Config:
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", None)
    # Get these values from my.telegram.org
    TG_COMPANION_BOT = os.environ.get("TG_BOT_TOKEN_BF_HER", None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # specify command handler that should be used for the plugins
    # this should be a valid "regex" pattern
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", "/")
    # This is required for the plugins involving the file system.
    TMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TMP_DOWNLOAD_DIRECTORY",
        "./DOWNLOADS/"
    )
    # get a Heroku API key from http://dashboard.heroku.com/account
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    # set this to your fork on GitHub (if you want)
    OFFICIAL_UPSTREAM_REPO = os.environ.get(
        "OFFICIAL_UPSTREAM_REPO",
        "https://github.com/SpEcHiDe/PyroGramUserBot"
    )
    # For Databases
    # can be None in which case plugins requiring
    # DataBase would not work
    DB_URI = os.environ.get("DATABASE_URL", None)
    # @NoOneCares
    TG_URI = int(os.environ.get("TELEGRAM_URL", "-100"))
    # gDrive variables
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    # SuDo User
    OWNER_ID = int(os.environ.get("OWNER_ID", "7351948"))
    # Array to store users who are authorized to use the bot
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    # the maximum number of 'selectable' messages in Telegram
    TG_MAX_SELECT_LEN = 100
    # for bakanup purposes
    TG_IRU_S_M_ID = int(os.environ.get("TG_IRU_S_M_ID", "0"))
    WARN_DATA_ID = int(os.environ.get("WARN_DATA_ID", "0"))
    WARN_SETTINGS_ID = int(os.environ.get("WARN_SETTINGS_ID", "0"))
    # message_id for the Pinned Message
    A_PIN_MESSAGE_ID = int(os.environ.get("A_PIN_MESSAGE_ID", "3"))
    #
    LAYER_FEED_CHAT = os.environ.get("LAYER_FEED_CHAT", None)
    LAYER_UPDATE_INTERVAL = os.environ.get("LAYER_UPDATE_INTERVAL", None)
    LAYER_UPDATE_MESSAGE_CAPTION = os.environ.get(
        "LAYER_UPDATE_MESSAGE_CAPTION",
        None
    )


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
