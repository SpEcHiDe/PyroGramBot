from pyrogram import filters
from pyrogram.types import Message
from pyrobot import (
    COMMAND_HAND_LER,
    A_PIN_MESSAGE_ID
)
from pyrobot.pyrobot import PyroBot


@PyroBot.on_message(
    filters.service
)
async def on_new_pin_message(client: PyroBot, message: Message):
    if message.pinned_message and message.pinned_message.message_id != A_PIN_MESSAGE_ID:
        original_pinned_message = await client.get_messages(
            chat_id=message.chat.id,
            message_ids=A_PIN_MESSAGE_ID
        )
        await original_pinned_message.pin(
            disable_notification=True
        )
@PyroBot.on_message(filters.pinned_message)
def pinned(c,m):
    m.delete()
