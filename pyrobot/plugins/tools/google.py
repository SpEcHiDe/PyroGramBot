"""
Google Search
Syntax: .google query
"""

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaDocument
from pyrobot import Config, COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import sudo_filter


@Client.on_message(
    filters.command("google", COMMAND_HAND_LER) &
    sudo_filter
)
async def google_(_, message: Message):
    if len(message.command) <= 1:
        return await message.reply_text(
            "എന്ത് ചെയ്യണം എന്ന് പറഞ്ഞില്ല!"
        )
    query = message.text.split(" ", maxsplit=1)[1]
    async with aiohttp.ClientSession() as requests:
        input_url = "https://bots.shrimadhavuk.me/search/"
        headers = {"USER-AGENT": "UseTGBot"}
        data = {
            "q": query,
            "app_id": Config.USE_TG_BOT_APP_ID
        }
        reponse = await requests.get(
            input_url,
            params=data,
            headers=headers
        )
        response = await reponse.json()
    text = f"Query: <code>{query}</code>\n"
    for result in response.get("results", []):
        title = result.get("title")
        url = result.get("url")
        # description = result.get("description")
        # image = result.get("image")
        text += f" 👉🏻  <a href='{url}'>{title}</a> \n\n"
    await message.reply_text(
        text,
        quote=True,
        disable_web_page_preview=True
    )


@Client.on_message(
    filters.command("gim", COMMAND_HAND_LER) &
    sudo_filter
)
async def google_image_(_, message: Message):
    if len(message.command) <= 1:
        return await message.reply_text(
            "എന്ത് ചെയ്യണം എന്ന് പറഞ്ഞില്ല!"
        )
    query = message.text.split(" ", maxsplit=1)[1]
    async with aiohttp.ClientSession() as requests:
        input_url = "https://bots.shrimadhavuk.me/search/"
        headers = {"USER-AGENT": "UseTGBot"}
        data = {
            "q": query,
            "app_id": Config.USE_TG_BOT_APP_ID,
            "p": "GoogleImages"
        }
        reponse = await requests.get(
            input_url,
            params=data,
            headers=headers
        )
        response = await reponse.json()
    text = f"Query: <code>{query}</code>\n"
    url_list = []
    for result in response.get("results", []):
        if len(url_list) > 9:
            break
        caption = result.get("description")
        image_url = result.get("url")
        url_list.append(
            InputMediaDocument(
                media=image_url,
                caption=caption
            )
        )
    await message.reply_media_group(
        url_list,
        quote=True
    )
