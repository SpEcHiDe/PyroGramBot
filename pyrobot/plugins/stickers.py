import os 
from os import error
import logging
import pyrogram
import random
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Sticker, Document


 DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")



@Client.on_message(filters.private & filters.command(["getsticker"]))
async def getsticker(bot, message):  
    tx = await message.reply_text("Checking Sticker")
    await tx.edit("Validating sticker..")
    await tx.delete()
    if message.reply_to_message is None: 
            tx =  await tx.edit("Reply to a Sticker File!")       
    else :
          if message.reply_to_message.sticker.is_animated:
             try :
                   tx = await message.reply_text("Downloading...")
                   file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.tgs"
                   await message.reply_to_message.download(file_path)  
                   await tx.edit("Downloaded") 
                #   zip_path= ZipFile.write("./DOWNLOADS/{message.chat.id}/tgs-{random_id}.tgs")
                   await tx.edit("Uploading...")
                   await message.reply_document(document=file_path,caption=f"©@BugHunterBots")
                   await tx.delete()   
                   os.remove(file_path)
                #   os.remove(zip_path)
             except Exception as error:
                   print(error)
 
          elif message.reply_to_message.sticker.is_animated is False:        
             try : 
                   tx = await message.reply_text("Downloading...")
                   file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.png"
                   await message.reply_to_message.download(file_path)   
                   await tx.edit("Downloaded")
                   await tx.edit("Uploading...")
                   await message.reply_document(document=file_path,caption=f"©@BugHunterBots")
                   await tx.delete()   
                   os.remove(file_path)
             except Exception as error:
                   print(error)

# © 2021 BugHunterCodeLabs
# @BugHunterBots

    
@Client.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**  \n `{message.reply_to_message.sticker.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("Oops !! Not a sticker file")
 
