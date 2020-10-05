from pyrogram import (
    Client,
    filters
)
from pyrobot import (
    COMMAND_HAND_LER,
    DB_URI,
    MAX_MESSAGE_LENGTH
)
from pyrobot.helper_functions.cust_p_filters import admin_fliter
if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.notes_sql as sql


@Client.on_message(
    filters.command(["clearnote", "clear"], COMMAND_HAND_LER) &
    admin_fliter
)
async def clear_note(_, message):
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )
    note_name = " ".join(message.command[1:])
    sql.rm_note(message.chat.id, note_name)
    await status_message.edit_text(
        f"note <u>{note_name}</u> deleted from current chat."
    )


@Client.on_message(
    filters.command(["listnotes", "notes"], COMMAND_HAND_LER)
)
async def list_note(_, message):
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )

    note_list = sql.get_all_chat_notes(message.chat.id)

    msg = "<b>Notes in {}:</b>\n".format("the current chat")
    msg_p = msg

    for note in note_list:
        note_name = " - #{}\n".format(note.name)
        if len(msg) + len(note_name) > MAX_MESSAGE_LENGTH:
            await message.reply_text(msg)
            msg = ""
        msg += note_name

    if msg == msg_p:
        await status_message.edit_text("ഇൗ ചാറ്റിൽ കുറിപ്പുകളൊന്നുമില്ല.")

    elif len(msg) != 0:
        await message.reply_text(msg)
        await status_message.delete()
