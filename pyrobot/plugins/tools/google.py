"""
Google Search 
https://serper.dev
free 1000 queries
"""

import requests
from pyrogram import Client, filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter
from pyrobot import Config

@Client.on_message(filters.command("google", COMMAND_HAND_LER) & sudo_filter)
async def google_(client, message):
    msg = await message.reply_text("Processing ..",True)
    if Config.SERPER_API is None:
	    return await msg.edit("SERPER_API is not set\n")
  
    query = message.text.split(" ", maxsplit=1)[1]
    
    headers = {
  'X-API-KEY': Config.SERPER_API,
  'Content-Type': 'application/json'
}
    params = {
  "q": query,
  "gl": "us", # default USA
  "hl": "en",
  "autocorrect": True
}
    req = requests.get("https://google.serper.dev/search",headers=headers, params=params)
    out = req.json()
    text = f"Query: `{query}`\n"
    try:
        for result in out['organic']:
           title = result["title"]
           link = result["link"]
           text += f"[{title}]({link})\n"
    except Exception as e:
	    print(e)
	    text += f"Failed to get results\n{e}"

    await msg.edit(text, disable_web_page_preview=True)
