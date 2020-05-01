from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.admin_check import AdminCheck
from pyrobot.helper_functions.extract_user import extract_user


@Client.on_message(Filters.command("unban", COMMAND_HAND_LER))
async def un_ban_user(client, message):
    is_admin = await AdminCheck(
        client,
        message.chat.id,
        message.from_user.id
    )
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
    except Exception as e:
        await message.reply_text(
            str(e)
        )
    else:
        if user_id.lower().startswith("@"):
            await message.reply_text(
                "ശരി, ബാൻ മാറ്റിയിട്ടുണ്ട്... ഇനി "
                f"{user_first_name} ക്ക് "
                " ഗ്രൂപ്പിൽ ചേരാൻ കഴിയും!"
            )
        else:
            await message.reply_text(
                "ശരി, ബാൻ മാറ്റിയിട്ടുണ്ട്... ഇനി "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> ക്ക് "
                " ഗ്രൂപ്പിൽ ചേരാൻ കഴിയും!"
            )
