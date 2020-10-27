from pyrogram import Client,filters


@Client.on_message(filters.service)
def service(c,m):
    m.delete()
