import json

from pyrogram.types import CallbackQuery

from pyrobot import COMMAND_HAND_LER, WARN_DATA_ID
from pyrobot.pyrobot import PyroBot


async def remove_warn(client: PyroBot, c_q: CallbackQuery, user_id: str, warner: int):
    chat_id = str(c_q.message.chat.id)

    if chat_id not in client.warndatastore:
        client.warndatastore[chat_id] = {}

    DATA = client.warndatastore[chat_id]

    if c_q.from_user.id == warner:
        if DATA.get(user_id):
            up_l = DATA[user_id]["limit"] - 1  # up_l = updated limit
            if up_l > 0:
                DATA[user_id]["limit"] = up_l
                del DATA[user_id]["reason"][-1]
            else:
                DATA.pop(user_id)
            mention = f"<a href='tg://user?id={c_q.from_user.id}'>{c_q.from_user.first_name}</a>"
            text = f"{mention} removed this Warn."
            await c_q.edit_message_text(text)
        else:
            await c_q.edit_message_text(
                "😕😕 This User does not have any Warn."
            )
        await c_q.answer() # ensure no spinny circle -_-
    else:
        await c_q.answer(
            f"Only {(await client.get_users(warner)).first_name} Can Remove this Warn",
            show_alert=True
        )

    client.warndatastore[chat_id] = DATA
    await client.save_public_store(
        WARN_DATA_ID,
        json.dumps(client.warndatastore)
    )
