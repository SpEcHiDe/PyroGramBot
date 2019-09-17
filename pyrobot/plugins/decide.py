from datetime import datetime

import pyrogram
import requests
from pyrogram import Client, Filters

from pyrobot import app, cmd


@app.on_message(Filters.command(["decide"], cmd) & Filters.me)
async def de_cide(client, message):
      message_id = message.message_id
      if message.reply_to_message:
         message_id = message.reply_to_message.message_id
      JSON = requests.get("https://yesno.wtf/api").json()
      await message.reply_animation(
            animation=JSON["image"],
            caption=JSON["answer"],
            reply_to_message_id=message_id
      )
      await message.delete()
