import os

class Config():
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", None)
    # Get these values from my.telegram.org
    # string session for running on Heroku
    # some people upload their session files on GitHub or other third party hosting
    # websites, this might prevent the un-authorized use of the
    # confidential session files
    HU_STRING_SESSION = os.environ.get("HU_STRING_SESSION", None)
    TG_COMPANION_BOT = os.environ.get("TG_BOT_TOKEN_BF_HER", None)
    #
    USE_AS_BOT = bool(os.environ.get("USE_AS_BOT", False))
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # specify command handler that should be used for the plugins
    # this should be a valid "regex" pattern
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", ".")
    # This is required for the plugins involving the file system.
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")
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
    TG_URI = os.environ.get("TELEGRAM_URL", "-100")
    # gDrive variables
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    # SuDo User
    OWNER_ID = int(os.environ.get("OWNER_ID", "7351948"))
    # Array to store users who are authorized to use the bot
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    # the maximum number of 'selectable' messages in Telegram
    TG_MAX_SELECT_LEN = int(os.environ.get("TG_MAX_SELECT_LEN", "100"))


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
