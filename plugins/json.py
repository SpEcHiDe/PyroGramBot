"""Get Detailed info about any message
Syntax: .json"""

from pyrogram import Client, Filters

import io

# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096


@Client.on_message(Filters.command("json", "{")  & Filters.me)
async def jsonify(client, message):
    the_real_message = None
    reply_to_id =  None

    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        the_real_message = message.reply_to_message
    else:
        the_real_message = message
        reply_to_id = message.message_id

    try:
        await message.edit(the_real_message)
    except Exception as e:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "json.text"
            await client.send_document(
                chat_id=message.chat.id,
                document=out_file,
                caption=str(e),
                disable_notification=True,
                reply_to_message_id=reply_to_id
            )
            await event.delete()
