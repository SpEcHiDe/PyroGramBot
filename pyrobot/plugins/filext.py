import pyrogram
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, Filters

from pyrobot import app, cmd


@app.on_message(Filters.command(["filext"], cmd) & Filters.me)
async def fil_ext(client, message):
      await message.edit("Processing ...")
      sample_url = "https://www.fileext.com/file-extension/{}.html"
      input_str = message.text[8:]
      response_api = requests.get(sample_url.format(input_str))
      status_code = response_api.status_code
      if status_code == 200:
          raw_html = response_api.content
          soup = BeautifulSoup(raw_html, "html.parser")
          ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
          await message.edit("File Extension: `{}`\nDescription: `{}`".format(input_str, ext_details))
          
      else:
        await message.edit("https://www.fileext.com/ responded with {} for query: {}".format(status_code, input_str))
