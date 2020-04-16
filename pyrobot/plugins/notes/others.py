from pyrogram import (
    Client,
    Filters
)

from pyrobot import (
    LOGGER,
    COMMAND_HAND_LER,
    DB_URI,
    MAX_MESSAGE_LENGTH
)

if DB_URI is not None:
    import pyrobot.helper_functions.sql_helpers.notes_sql as sql


from pyrobot.helper_functions.admin_check import AdminCheck


@Client.on_message(Filters.command("clearnote", COMMAND_HAND_LER))
async def clear_note(client, message):
    is_admin = await AdminCheck(
        client,
        message.chat.id,
        message.from_user.id
    )
    if not is_admin:
        return
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )
    note_name = " ".join(message.command[1:])
    sql.rm_note(message.chat.id, note_name)
    await status_message.edit_text(
        f"note <u>{note_name}</u> deleted from current chat."
    )


@Client.on_message(Filters.command("listnotes", COMMAND_HAND_LER))
async def list_note(client, message):
    status_message = await message.reply_text(
        "checking 🤔🙄🙄",
        quote=True
    )

    note_list = sql.get_all_chat_notes(message.chat.id)

    msg = "<b>Notes in {}:</b>\n".format("the current chat")
    msg_p = msg

    for note in note_list:
        note_name = " - {}\n".format(note.name)
        if len(msg) + len(note_name) > MAX_MESSAGE_LENGTH:
            await message.reply_text(msg)
            msg = ""
        msg += note_name

    if msg == msg_p:
        await status_message.edit_text("ഇൗ ചാറ്റിൽ കുറിപ്പുകളൊന്നുമില്ല.")

    elif len(msg) != 0:
        await message.reply_text(msg)
        await status_message.delete()