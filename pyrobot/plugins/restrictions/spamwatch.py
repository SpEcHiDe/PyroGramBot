import asyncio
import logging
import os

import pyrogram
from pyrogram import Client, Filters
from pyrogram.api import functions, types
from pyrogram.errors import *
import spamwatch

from pyrobot import SPAMWATCH_API,LOGGER_GROUP

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
admin = 'administrator'
creator = 'creator'
ranks = [admin, creator]



async def AdminCheck(message):
    SELF = await pyrogram.Client.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id)

    if SELF.status not in ranks:
        await message.edit("__I'm not Admin!__")
        await asyncio.sleep(2)
        await message.delete()

    else:
        if SELF.status is not admin:
            return True
        elif SELF.permissions.can_restrict_members:
            return True
        else:
            await message.edit("__No permissions to restrict Members__")

async def RestrictFailed(message):
    await message.edit(f"I can't {message.command[0]} this user.")

@Client.on_message(~Filters.me & Filters.group & (Filters.text | Filters.new_chat_members))
async def user_list(client: Client, message):
    try:
        if message.service:
            if message.new_chat_members:
                chat_id = message.chat.id
                user_id = message.new_chat_members[0].id
                firstname = message.new_chat_members[0].first_name
        elif message.from_user:
            chat_id = message.chat.id
            user_id = message.from_user.id
            firstname = message.from_user.first_name
    except Exception:
        return  
    if SPAMWATCH_API is not None:
        try:
            
            WATCH = spamwatch.Client(SPAMWATCH_API)
            intruder = WATCH.get_ban(user_id)
            if intruder and await AdminCheck(message):
                await client.kick_chat_member(chat_id, user_id)
                txt = r"\\**#Antispam_Log**//" \
                    "\n\n**GBanned User $SPOTTED**\n" \
                    "**#SPAMWATCH_API BAN**" \
                    f"\n**User:** [{firstname}](tg://user?id={user_id})\n" \
                    f"**ID:** `{user_id}`\n**Reason:** `{intruder.reason}`\n" \
                    "**Quick Action:** Banned in {message.chat.title}\n\n$AUTOBAN #id{user_id}"
                await client.send_message(
                    chat_id=LOGGER_GROUP,
                    text=txt  
                )
        except Exception:
            pass
