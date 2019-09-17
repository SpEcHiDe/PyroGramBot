import os
import time
from datetime import datetime

import pyrogram
from pyrogram import Client, Filters
from pyrogram.api import functions

from pyrobot import app, cmd
from pyrobot.plugins.display import progress_for_pyrogram

timesleep = 1
thumb_image_path = "./DOWNLOADS/thumb.jpg"

@app.on_message(Filters.command(["upload"], cmd) & Filters.me)
async def telegram_upload(client, message):
      msg = await message.edit("Processing ...")
      fname = message.text[8:]
      print(fname)
      thumb = None
      if os.path.exists(thumb_image_path):
         thumb = thumb_image_path
      if os.path.exists(fname):
         start = datetime.now()
         c_time = time.time()
         await message.reply_document(
               document=fname,
               quote=True,
               thumb=thumb,
               #caption="@HK_ROBOT",
               parse_mode="HTML",
               progress=progress_for_pyrogram,
               progress_args=(
                    msg,c_time, "Uploading... "
                )
         )
         end = datetime.now()
         ms = (end - start).seconds
         await msg.edit("Uploaded in {} seconds.".format(ms))
      else:
           await msg.edit("404: File Not Found")
           time.sleep(5)
           await msg.delete()
