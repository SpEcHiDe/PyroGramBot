import asyncio
import math
import os
import time
from datetime import datetime

import aiohttp
import pyrogram
from pyrogram import Client, Filters
from pySmartDL import SmartDL

from pyrobot import app, cmd
from pyrobot.plugins.display import humanbytes, progress_for_pyrogram

DOWNLOAD_LOCATION= "./DOWNLOADS/"

@app.on_message(Filters.command(["download"], cmd) & Filters.me)
async def download_telegram(client, message):
      mone = await message.edit("Processing ...") # Reply
      url = message.text[10:]
      if message.reply_to_message:
         start = datetime.now()
         c_time = time.time()
         try:
             downloaded_file_name = await message.reply_to_message.download(
                                    file_name=DOWNLOAD_LOCATION,
                                    progress=progress_for_pyrogram,
                                    progress_args=(
                                                   mone,c_time, "Downloading... "
             )
             )
             downloaded_file_name=downloaded_file_name[4:]
             downloaded_file_name="."+downloaded_file_name
         except Exception as e: 
             await mone.edit(str(e))
         else:
             end = datetime.now()
             ms = (end - start).seconds
             await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
             # time.sleep(100000)
             # await mone.delete()
      
      elif url:
           start = datetime.now()
           file_name = os.path.basename(url)
           to_download_directory = "./DOWNLOADS/"
           if "|" in url:
               url, file_name = url.split("|")
           url = url.strip()
           file_name = file_name.strip()
           downloaded_file_name = os.path.join(to_download_directory, file_name)
           downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
           downloader.start(blocking=False)
           display_message = ""
           c_time = time.time()
           while not downloader.isFinished():
                 total_length = downloader.filesize if downloader.filesize else None
                 downloaded = downloader.get_dl_size()
                 now = time.time()
                 diff = now - c_time
                 percentage = downloader.get_progress() * 100
                 speed = downloader.get_speed()
                 elapsed_time = round(diff) * 1000
                 progress_str = "[{0}{1}]\nProgress: {2}%".format(
                          ''.join(["█" for i in range(math.floor(percentage / 5))]),
                          ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
                          round(percentage, 2))
                 estimated_total_time = downloader.get_eta(human=True)
                 try:
                    current_message = f"trying to download\n"
                    current_message += f"URL: {url}\n"
                    current_message += f"File Name: {file_name}\n"
                    current_message += f"{progress_str}\n"
                    current_message += f"{humanbytes(downloaded)} of {humanbytes(total_length)}\n"
                    current_message += f"ETA: {estimated_total_time}"
                    if round(diff % 10.00) == 0 and current_message != display_message:
                       await mone.edit(current_message)
                       display_message = current_message
                 except Exception as e:
                       await mone.edit(str(e))
           end = datetime.now()
           ms = (end - start).seconds
           if downloader.isSuccessful():
              await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
           else:
              await mone.edit("Incorrect URL\n {}".format(url))
      
      else:
           await mone.edit("Reply to a message to download to my local server.")
           time.sleep(5)
           await mone.delete()
