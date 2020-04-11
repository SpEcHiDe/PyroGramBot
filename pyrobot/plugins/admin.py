
import asyncio
import logging
import math
import os
from asyncio import sleep
from datetime import datetime
from os import remove
from time import sleep, time

import pyrogram
from pyrogram import ChatMember, Client, Filters, Message
from pyrogram.api import functions, types
from pyrogram.api.functions.channels import (EditAdmin, EditBanned,
                                             EditCreator, EditPhoto,
                                             TogglePreHistoryHidden)
from pyrogram.api.functions.messages import EditChatAdmin, EditChatPhoto
from pyrogram.api.types import (ChannelParticipantAdmin,
                                ChannelParticipantCreator, ChatAdminRights,
                                ChatBannedRights, ChatParticipant,
                                ChatParticipantAdmin, InputChannelEmpty,
                                InputChannelFromMessage, InputPeerChat,
                                UpdateChannelPinnedMessage,
                                UpdateChatPinnedMessage)
from pyrogram.errors import *

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY

from ..helper_functions.invervalhelper import IntervalHelper
from ..helper_functions.log_message import LogMessage

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

logger = logging.getLogger(__name__)

admin = 'administrator'
creator = 'creator'
ranks = [admin, creator]

BANNED = "{0.reply_to_message.from_user.first_name} has been banned."
BANNED_TIME = (
    "{0.reply_to_message.from_user.first_name} has been banned for {1}.")
BANNED_LOG = (
    "[{0.reply_to_message.from_user.first_name}](tg://user?id={0.reply_to_message.from_user.id}) "
    "has been banned from \"[{0.chat.title}](t.me/c/{1}/{0.message_id})\".")

UNBANNED = "{0.message.reply_to_message.from_user.first_name} has been unbanned"
UNBANNED_LOG = (
    "[{0.reply_to_message.from_user.first_name}](tg://user?id="
    "{0.reply_to_message.from_user.id}) has been unbanned in \"["
    "{0.chat.title}](t.me/c/{1}/{0.message_id})\".")

MUTED = "{0.reply_to_message.from_user.first_name} has been muted."
MUTED_TIME = "{0.reply_to_message.from_user.first_name} has been muted for {1}."
MUTED_LOG = (
    "[{0.reply_to_message.from_user.first_name}](tg://user?id={0.reply_to_message.from_user.id}) "
    "has been muted in \"[{0.chat.title}](t.me/c/{1}/{0.message_id})\".")

UNMUTED = "{0.reply_to_message.from_user.first_name} has been unmuted."
UNMUTED_LOG = (
    "[{0.reply_to_message.from_user.first_name}](tg://user?id={0.reply_to_message.from_user.id}) "
    "has been unmuted in \"[{0.chat.title}](t.me/c/{1}/{0.message_id})\".")

KICKED = "{0.reply_to_message.from_user.first_name} has been kicked."
KICKED_LOG = (
    "[{0.reply_to_message.from_user.first_name}](tg://user?id={0.reply_to_message.from_user.id}) "
    "has been kicked from \"[{0.chat.title}](t.me/c/{1}/{0.message_id})\".")

def Timer(message: Message):
    if len(message.command) > 1:
        secs = IntervalHelper(message.command[1])
        return int(str(time()).split(".")[0]) + secs.to_secs()[0]
    else:
        return 0


def TimerString(message: Message):
    secs = IntervalHelper(message.command[1])
    return f"{secs.to_secs()[1]} {secs.to_secs()[2]}"

async def ReplyCheck(message):
    if not message.reply_to_message:
        await message.edit(f"`{message.command[0]}` needs to be a reply.")
        await asyncio.sleep(2)
        await message.delete()
    elif message.reply_to_message.from_user.is_self:
        await message.edit(f"I can't {message.command[0]} myself.")
        await asyncio.sleep(2)
        await message.delete()
    else:
        return True

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


@Client.on_message(Filters.command(r"setgic", ".")  & Filters.me)
async def set_gic(client: Client, message):
    peer = await client.resolve_peer(message.chat.id)
    if not message.text.isalpha() and message.text not in ("/", "!"):
        if message.reply_to_message.message_id:
            reply_message = message.reply_to_message.message_id
    await message.edit("Downloading Profile Picture to my local ...")
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):  
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)   
    photo = None
    try:
        photo = await client.download_media(
            message=message.reply_to_message,
            file_name=TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e: 
        await message.edit(str(e))
    else:
        if photo:
            await message.edit("now, Uploading to group pic ...")
            try:
                photo = types.InputChatUploadedPhoto(file=await client.save_file(photo))
                await client.send(
                    functions.messages.EditChatPhoto(
                        chat_id=peer.chat_id,
                        photo=photo
                    )
                )
            except Exception as e:  
                await message.edit(str(e))
            else:
                await message.edit("Group profile picture was succesfully changed")
    try:
        os.remove(photo)
    except Exception as e:  
        logger.warnning(str(e)) 



@Client.on_message(Filters.command("ban", COMMAND_HAND_LER)  & Filters.me)
async def bann(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        if await ReplyCheck(message) is True:
            name = message.reply_to_message.from_user.first_name
            user_id = message.reply_to_message.from_user.id
            try:
                await client.kick_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    until_date=0
                )
                await message.edit("[{}](tg://user?id={}) banned!".format(name,user_id))
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message.reply_to_message.message_id
                )
            except UserAdminInvalid:
                RestrictFailed(message)


@Client.on_message(Filters.command("unban", COMMAND_HAND_LER)  & Filters.me)
async def unbann(client: Client, message):
    print(message)
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        if await ReplyCheck(message) is True:
            name = message.reply_to_message.from_user.first_name
            user_id = message.reply_to_message.from_user.id
            try:
                await client.unban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id
                )
                await message.edit("[{}](tg://user?id={}) unbanned!".format(name,user_id))
            except UserAdminInvalid:
                RestrictFailed(message)



@Client.on_message(Filters.command("promote", COMMAND_HAND_LER)  & Filters.me)
async def promot(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if await ReplyCheck(message) is True:
        if SELF.status in ranks:
            try:
                x = await client.promote_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id,
                    can_change_info=False,
                    can_delete_messages=1,
                    can_invite_users=1,
                    can_pin_messages=1,
                    can_promote_members=False,
                    can_restrict_members=1
                )
                if x:
                    await message.edit("`Successfully promoted.`")
            except PermissionError:
                await RestrictFailed(message)

@Client.on_message(Filters.command("demote", COMMAND_HAND_LER)  & Filters.me)
async def demot(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if await ReplyCheck(message) is True:
        if SELF.status in ranks:
            try:
                x = await client.promote_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id,
                    can_change_info=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_restrict_members=False
                )
                if x:
                    await message.edit("`Successfully demoted.`")
            except PermissionError:
                await RestrictFailed(message)

@Client.on_message(Filters.command('botlist', COMMAND_HAND_LER) & Filters.me )
async def bot_list(client: Client, message):
    try:
        bots = "\n"
        async for member in client.iter_chat_members(message.chat.id,filter="bots"):
            bots += "🤖 [{}](tg://user?id={})\n".format(member.user.first_name,member.user.id)
        await message.edit("Botlist in {}\n{}".format(message.chat.title,bots))
    except MessageTooLong:
        await message.edit(
            "This group is filled with bots as hell. Uploading bots list as file."
        )
        with open('botlist.txt', 'w') as file:
            file.write(bots)
            file.close()
        await client.send_document(
            chat_id=message.chat.id,
            document="botlist.txt",
            caption='Bots in {}'.format(message.chat.title),
            reply_to_message_id=message.message_id,
        )
        os.remove("botlist.txt")


@Client.on_message(Filters.command('adminlist', COMMAND_HAND_LER) & Filters.me )
async def admin_list(client: Client, message):
    try:
        admins = "\n"
        async for member in client.iter_chat_members(message.chat.id,filter="administrators"):
            admins += "⭐️ [{}](tg://user?id={})\n".format(name,admin_id)
        await message.edit("Admin in **{}**\n{}".format(message.chat.title,admins))
    except MessageTooLong:
        await message.edit(
            "This group is filled with bots as hell. Uploading bots list as file."
        )
        with open('adminlist.txt', 'w') as file:
            file.write(admins)
            file.close()
        await client.send_document(
            chat_id=message.chat.id,
            document="adminlist.txt",
            caption='Admins in {}'.format(message.chat.title),
            reply_to_message_id=message.message_id,
        )
        os.remove("adminlist.txt")


@Client.on_message(Filters.command('userlist', COMMAND_HAND_LER) & Filters.me )
async def user_list(client: Client, message):
    try:
        users = "\n"
        async for member in client.iter_chat_members(message.chat.id):
            users += "👉 [{}](tg://user?id={})\n".format(member.user.first_name,member.user.id)
        await message.edit("Users in **{}**\n{}".format(message.chat.title,users))
    except MessageTooLong:
        await message.edit(
            "This group is filled with bots as hell. Uploading bots list as file."
        )
        with open('userslist.txt', 'w') as file:
            file.write(users)
            file.close()
        await client.send_document(
            chat_id=message.chat.id,
            document="userlist.txt",
            caption='users in {}'.format(message.chat.title),
            reply_to_message_id=message.message_id,
        )
        os.remove("userslist.txt")


@Client.on_message(Filters.command('ghostlist', COMMAND_HAND_LER) & Filters.me  )
async def ghost_list(client: Client, message):
    try:
        deleted = []
        async for member in client.iter_chat_members(message.chat.id):
            if member.user.is_deleted:
                deleted.append("👻 [{}](tg://user?id={})\n".format(member.user.first_name,member.user.id))
        print(len(deleted))
        await message.edit("{} Deleted Accounts Detected in {}".format(len(deleted),message.chat.title))
    except MessageTooLong:
        await message.edit(
            "This group is filled with deleted account as hell. Uploading bots list as file."
        )
        with open('deleted_account.txt', 'w') as file:
            file.write(deleted)
            file.close()
        await client.send_document(
            chat_id=message.chat.id,
            document="deleted_account.txt",
            caption='Deleted Account in {}'.format(message.chat.title),
            reply_to_message_id=message.message_id,
        )
        os.remove("deleted_account.txt")
        


@Client.on_message(Filters.command("mute", COMMAND_HAND_LER)  & Filters.me)
async def mutee(client: Client, message):
    print(message)
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        if await ReplyCheck(message) is True:
            try:
                await client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    until_date=Timer(message),
                    can_send_messages=False,)
                if len(message.command) > 1:
                    await message.edit(MUTED_TIME.format(
                        message,
                        TimerString(message)))
                else:
                    await message.edit(MUTED.format(message))
            except UserAdminInvalid:
                RestrictFailed(message)

            

@Client.on_message(Filters.command("kick", COMMAND_HAND_LER)  & Filters.me)
async def kick(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        if await ReplyCheck(message) is True:
            try:
                await client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    until_date=0,
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
                await message.edit(UNMUTED.format(message))
                LogMessage(UNMUTED_LOG.format(
                    message,
                    str(message.chat.id).replace("-100", "")))
            except UserAdminInvalid:
                RestrictFailed(message)


@Client.on_message(Filters.command("cclean", COMMAND_HAND_LER) & Filters.me)
async def clean_deleted(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        await message.edit("`Cleaning deleted accounts in this chat..`")
        all_members = await client.iter_chat_members(message.chat.id)
        to_remove = []
        removed = []

        async for member in all_members:
            if member.user.is_deleted:
                to_remove.append(member.user.id)

        await message.edit(f"`{len(to_remove)} deleted accounts found.`")

        async for usr in to_remove:
            try:
                await client.kick_chat_member(
                    chat_id=message.chat.id,
                    user_id=usr
                )
                removed.append(usr)
            except UserAdminInvalid:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.x)
        await message.edit(f"Removed {len(removed)} deleted accounts.")






@Client.on_message(Filters.command("pin", COMMAND_HAND_LER) & Filters.me)
async def pin(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        if message.reply_to_message.message_id:
            try:
                await client.pin_chat_message(
                    chat_id=message.chat.id,
                    message_id=message.reply_to_message.message_id,
                    disable_notification=False
                )
                await message.edit("`Pinned successfully.`")
            except RPCError:
                pass

@Client.on_message(Filters.command("undlt", COMMAND_HAND_LER) & Filters.me)
async def undlt(client: Client, message):
    deleted_msg = "Deleted 10 Messages in {}\n".format(message.chat.title)
    async for msg in client.iter_history(chat_id=message.chat.id,limit=10,reverse=False):
        deleted_msg += "👉 {}\n".format(msg.text)
    await message.edit(deleted_msg)

