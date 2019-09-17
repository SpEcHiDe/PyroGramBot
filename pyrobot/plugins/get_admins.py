import pyrogram
from pyrogram import Client, Filters

from pyrobot import app, cmd


@app.on_message(Filters.command(["get_admin"], cmd) & Filters.me)
async def get_admins(client, message):
      mentions = "Admin List: \n"
      input_str = message.text[11:]
      if not input_str:
         input_str = message.chat.id
      try:
         async for x in client.iter_chat_members(chat_id=input_str, filter="administrators"):
               if x.status == "creator":
                   mentions += "\n 👑 [{}](tg://user?id={}) `{}`".format(x.user.first_name, x.user.id, x.user.id)
               if x.status == "administrator":
                   mentions += "\n ⚜ [{}](tg://user?id={}) `{}`".format(x.user.first_name, x.user.id, x.user.id)
      except Exception as e:
             mentions += " " + str(e) + "\n"
      await message.edit(mentions)
      
@app.on_message(Filters.command(["men_admin"], cmd) & Filters.me)
async def men_admins(client, message):
      mentions = "Admin List: \n"
      input_str = message.text[11:]
      if not input_str:
         input_str = message.chat.id
      try:
         async for x in client.iter_chat_members(chat_id=input_str, filter="administrators"):
               if x.status == "creator":
                   mentions += "\n 👑 [{}](tg://user?id={}) `{}`".format(x.user.first_name, x.user.id, x.user.id)
               if x.status == "administrator":
                   mentions += "\n ⚜ [{}](tg://user?id={}) `{}`".format(x.user.first_name, x.user.id, x.user.id)
      except Exception as e:
             mentions += " " + str(e) + "\n"
      await message.reply(mentions)
      await message.delete()
