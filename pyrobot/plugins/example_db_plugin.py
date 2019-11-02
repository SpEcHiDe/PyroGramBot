"""Example DB Plugin"""

from pyrogram import Client, Filters

import os

from pyrobot import MAX_MESSAGE_LENGTH, COMMAND_HAND_LER, DB_CHAT_ID, DB_MESG_ID
from pyrobot.helper_functions.db_storage import load_db, save_db


@Client.on_message(Filters.command("testeg", COMMAND_HAND_LER)  & Filters.me)
async def example_db_plugin(client, message):
    if DB_CHAT_ID is None or DB_MESG_ID is None:
        await message.edit("DB variable is not configured. Quiting.")
        return
    test_update = {}
    # if "example" not in test_update.keys():
    #     test_update["example"] = {}
    # test_update["example"]["key"] = "value one"
    # test_update["example"]["key two"] = "value two"
    # if "example two" not in test_update.keys():
    #     test_update["example two"] = {}
    # test_update["example two"]["key"] = "value one"
    # if "example three" not in test_update.keys():
    #     test_update["example three"] = {}
    # test_update["example three"]["key two"] = "value two"
    await save_db(client, DB_CHAT_ID, DB_MESG_ID, test_update)
    example_saved_db = await load_db(client, DB_CHAT_ID, DB_MESG_ID)
    print(example_saved_db)
