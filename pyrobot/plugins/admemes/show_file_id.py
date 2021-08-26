"""Get id of the replied user
Syntax: .id"""

from pyrogram import Client, filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter
from pyrobot.helper_functions.get_file_id import get_file_id


@Client.on_message(
    filters.command(["id"], COMMAND_HAND_LER) &
    f_onw_fliter
)
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"<code>{user_id}</code>",
            quote=True
        )

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += (
            "<b>Chat ID</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>Replied User ID</b>: "
                f"<code>{message.reply_to_message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        else:
            _id += (
                "<b>User ID</b>: "
                f"<code>{message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        await message.reply_text(
            _id,
            quote=True
        )
