"""Purge Messages
Syntax: .purge"""

import asyncio
from datetime import datetime

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER

from pyrobot.helper_functions.admin_check import AdminCheck


@Client.on_message(Filters.command("purge", COMMAND_HAND_LER))
async def purge(client, message):
    is_admin = await AdminCheck(
        client,
        message.chat.id,
        message.from_user.id
    )
    if not is_admin:
        return
    # TODO: -_-