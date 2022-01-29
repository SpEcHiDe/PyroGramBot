from pyrogram import Client, filters
from pyrobot import COMMAND_HAND_LER
from pyrobot.helper_functions.extract_user import extract_user
from pyrobot.helper_functions.cust_p_filters import admin_fliter


@Client.on_message(
    filters.command(["unban", "unmute"], COMMAND_HAND_LER) &
    admin_fliter
)
async def un_ban_user(_, message):
    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "ശരി, മാറ്റിയിട്ടുണ്ട്... ഇനി "
                f"{user_first_name} ക്ക് "
                " ഗ്രൂപ്പിൽ ചേരാൻ കഴിയും!"
            )
        else:
            await message.reply_text(
                "ശരി, മാറ്റിയിട്ടുണ്ട്... ഇനി "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> ക്ക് "
                " ഗ്രൂപ്പിൽ ചേരാൻ കഴിയും!"
            )
