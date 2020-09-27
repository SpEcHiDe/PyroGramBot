from pyrogram import Client, filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.string_handling import extract_time


@Client.on_message(filters.command("ban", COMMAND_HAND_LER))
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


@Client.on_message(filters.command("tban", COMMAND_HAND_LER))
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "അസാധുവായ സമയ തരം വ്യക്തമാക്കി. "
                "പ്രതീക്ഷിച്ചതു m, h, or d, കിട്ടിയത്: {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.kick_member(
            user_id=user_id,
            until_date=until_date_val
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
                f" banned for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "വേറെ ഒരാളും പൊടി പാറിപ്പിക്കുന്നു..! "
                f"<a href='tg://user?id={user_id}'>"
                "ലവനെ"
                "</a>"
                f" banned for {message.command[1]}!"
            )
