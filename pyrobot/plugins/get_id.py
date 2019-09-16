import pyrogram
from pyrogram import Filters, Client
from pyrobot import app, cmd

@app.on_message(Filters.command(["get_id"], cmd) & Filters.me)
async def get_ids(client, message):
      if message.reply_to_message:
         chat = message.reply_to_message.from_user.id
         file_id = None
         if message.reply_to_message.media:
            if message.reply_to_message.audio:
               file_id = message.reply_to_message.audio.file_id
            elif message.reply_to_message.document:
               file_id = message.reply_to_message.document.file_id
            elif message.reply_to_message.photo:
               file_id = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
               file_id = message.reply_to_message.sticker.file_id
            elif message.reply_to_message.voice:
               file_id = message.reply_to_message.voice.file_id
            elif message.reply_to_message.video_note:
               file_id = message.reply_to_message.video_note.file_id
            elif message.reply_to_message.video:
               file_id=message.reply_to_message.video.id
         if file_id is not None:
             await message.edit("Current Chat ID: `{}`\nFrom User ID: `{}`\nFile ID: `{}`".format(str(message.chat.id), str(chat), file_id))
         else:
             await message.edit("Current Chat ID: `{}`\nFrom User ID: `{}`".format(str(message.chat.id), str(chat)))
      else:
           await message.edit("Current Chat ID: `{}`".format(str(message.chat.id)))
            
         
