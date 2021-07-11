# https://github.com/bughunter0/Pyrogram-tts-Bot
# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os 
from os import error
import logging
import pyrogram
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message
from gtts import gTTS 

@Client.on_message(filters.command(["tts"]))
async def tts(bot, message):
  try:
      text = str(message.reply_to_message.text)
      language = 'en-in'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                          # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
      tts_file = gTTS(text=text, lang=language, slow=False) 
      tts_file.save(f"{message.chat.id}.mp3") 
      chat_id = str(message.chat.id)
      with open(f"{message.chat.id}.mp3", "rb") as speech:
           await bot.send_voice(chat_id, speech, caption ="@BugHunterBots")
      os.remove(f"{message.chat.id}.mp3")
  except Exception as error:
       print (error)
