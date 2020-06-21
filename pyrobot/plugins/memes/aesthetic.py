from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER

from pyrobot.helper_functions.cust_p_filters import f_onw_fliter


def aesthetify(string):
    PRINTABLE_ASCII = range(0x21, 0x7f)
    for c in string:
        c = ord(c)
        if c in PRINTABLE_ASCII:
            c += 0xFF00 - 0x20
        elif c == ord(" "):
            c = 0x3000
        yield chr(c)


@Client.on_message(Filters.command(["ae"], COMMAND_HAND_LER)  & f_onw_fliter)
async def aesthetic(client, message):
    status_message = await message.reply_text("...")
    text = "".join(str(e) for e in message.command[1:])
    text = "".join(aesthetify(text))
    await status_message.edit(text)
