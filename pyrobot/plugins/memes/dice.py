# EMOJI CONSTANTS
DICE_E_MOJI = "🎲"
# EMOJI CONSTANTS

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER


@Client.on_message(Filters.command("roll", COMMAND_HAND_LER))
async def jsonify(client, message):
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=DICE_E_MOJI,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id
    )
