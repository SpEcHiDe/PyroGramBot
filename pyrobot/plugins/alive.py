from pyrogram import Filters, Message

from pyrobot import START_TIME, app, cmd

ALIVE = f"I'm working from {START_TIME} and i am still alive."

@app.on_message(Filters.command("alive", cmd) & Filters.me)
async def _alive(bot: app, message: Message):
      await message.edit(ALIVE)
