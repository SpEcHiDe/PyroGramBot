from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.extract_user import extract_user


@Client.on_message(Filters.command("ban", COMMAND_HAND_LER))
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.kick_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"{user_first_name}"
                " നെ വിലക്കിയിരിക്കുന്നു."
            )
        else:
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a>"
                " നെ വിലക്കിയിരിക്കുന്നു."
            )
