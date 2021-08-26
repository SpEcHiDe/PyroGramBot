# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os , glob
from os import error
import logging
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Sticker, Document

@Client.on_message(filters.command(["findsticker"]))
async def findsticker(bot, message):  
  try:
        txt = await message.reply_text("Validating Sticker ID")
        stickerid = str(message.reply_to_message.text)
        chat_id = int(message.chat.id)
        await txt.delete()
        await bot.send_sticker(chat_id,f"{stickerid}")
  except Exception as error:
        txt = await message.reply_text("Not a Valid File ID")
