"""Profile Updation Commands
.pbio <Bio>
.pname <Name>
.ppic"""
import logging
import os
from datetime import datetime

from pyrogram import Client, Filters
from pyrogram.api import functions, types
from pyrogram.api.functions.account import UpdateProfile
from pyrogram.api.functions.photos import UpdateProfilePhoto

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

@Client.on_message(Filters.command(r"pbio", ".")  & Filters.me)
async def test(client, message):
    bio = message.command[1]
    try:
        await client.send(functions.account.UpdateProfile(about=bio))
        await message.edit("Succesfully changed my profile bio")
    except Exception as e: 
        await message.edit(str(e))


@Client.on_message(Filters.command(r"pname", ".")  & Filters.me)
async def name(client, message):
    names = message.command[1]
    print(message)
    name_first = names
    name_last = ""
    if  "\\n" in names:
        first_name, last_name = names.split("\\n", 1)
    try:
        await client.send(UpdateProfilePhoto())
        await client.send(functions.account.UpdateProfile(first_name=name_first, last_name=name_last))
        await message.edit("My name was changed successfully")
    except Exception as e:  
        await message.edit(str(e))


@Client.on_message(Filters.command(r"ppic", ".")  & Filters.me)
async def profile_pic(client, message):
    print(message)
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
            await message.edit("now, Uploading to @Telegram ...")
            try:
                await client.send(
                    functions.photos.UploadProfilePhoto(
                    file=await client.save_file(photo)
                    )
                )
            except Exception as e:  
                await message.edit(str(e))
            else:
                await message.edit("My profile picture was succesfully changed")
    try:
        os.remove(photo)
    except Exception as e:  
        logger.warn(str(e))  

@Client.on_message(Filters.command(r"profilephoto", ".")  & Filters.me)
async def _(client, message):
    """getting user profile photo last changed time"""
    p_number = message.command[1]
    print(p_number)
    try:
        a = await message.edit("getting profile pic changed or added date")
        photos = await client.get_profile_photos(message.chat.id)
        msg = datetime.fromtimestamp(photos[int(p_number)].date).strftime('%d-%m-%Y')
        msg = "Last profile photo changed: \n👉 `{}` UTC+3".format(str(msg))
        await a.edit(msg)
    except :
        pass
