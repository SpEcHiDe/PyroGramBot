import logging

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
PRINTABLE_ASCII = range(0x21, 0x7f)


def aesthetify(string):
    for c in string:
        c = ord(c)
        if c in PRINTABLE_ASCII:
            c += 0xFF00 - 0x20
        elif c == ord(" "):
            c = 0x3000
        yield chr(c)


@Client.on_message(Filters.command(["ae"], COMMAND_HAND_LER)  & Filters.me)
async def aesthetic(client, message):
    text = "".join(str(e) for e in message.command[1:])
    text = "".join(aesthetify(text))
    await message.edit(text)
