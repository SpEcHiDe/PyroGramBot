import os , glob
from os import error
import logging
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Sticker, Document


@bughunter0.on_message(filters.private & filters.command(["getsticker"]))
async def getstickerasfile(bot, message):  
    if message.reply_to_message is None: 
               tx =  await tx.edit("Reply to a Sticker File!")       
          else :
               if message.reply_to_message.sticker.is_animated:
                   try :     
                        tx = await message.reply_text("Downloading...")
                        file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.tgs"
                        await message.reply_to_message.download(file_path)  
                        await tx.edit("Downloaded") 
                    #   zip_path= ZipFile.write("")
                        await tx.edit("Uploading...")
                        start = time.time()
                        await message.reply_document(file_path,caption="©@BugHunterBots")
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
                       start = time.time()
                       await message.reply_document(file_path,caption="©@BugHunterBots")
                       await tx.delete()   
                       os.remove(file_path)
                   except Exception as error:
                       print(error)
