from pyrogram import filters
from pyrobot import (
    COMMAND_HAND_LER,
    LOGGER,
    MAX_MESSAGE_LENGTH,
    TG_URI,
    TG_IRU_S_M_ID
)
from pyrobot.pyrobot import PyroBot
from pyrobot.helper_functions.admin_check import admin_check
from pyrobot.helper_functions.cust_p_filters import f_onw_fliter



@PyroBot.on_message(
    filters.command(["clearfilter"], COMMAND_HAND_LER) &
    f_onw_fliter
)
async def clear_filter(client: PyroBot, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )
    flt_name = " ".join(message.command[1:])
    flt_list = client.publicstore.get(str(message.chat.id), [])
    flt_list.pop(flt_name)
    await client.save_public_store()
    await status_message.edit_text(
        f"filter <u>{flt_name}</u> deleted from current chat."
    )


@PyroBot.on_message(
    filters.command(["listfilters", "filters"], COMMAND_HAND_LER)
)
async def list_filters(client: PyroBot, message):
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )
    flt_list = client.publicstore.get(str(message.chat.id), [])
    msg = "<b>Filters in {}:</b>\n".format("the current chat")
    msg_p = msg
    for flt in flt_list:
        flt_name = " - {}\n".format(flt)
        if len(msg) + len(flt_name) > MAX_MESSAGE_LENGTH:
            await message.reply_text(msg)
            msg = ""
        msg += f"{flt_name}"
    if msg == msg_p:
        await status_message.edit_text("ഇൗ ചാറ്റിൽ കുറിപ്പുകളൊന്നുമില്ല.")

    elif len(msg) != 0:
        await message.reply_text(msg)
        await status_message.delete()
