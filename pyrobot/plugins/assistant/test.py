from pyrogram import Client, filters

# @Client.on_message(
#     filters.private &
#     filters.via_bot
# )
# async def _(_, m):
#     print(m)
#     await m.reply(str(m.media))


# @Client.on_message(
#     filters.private &
#     filters.via_bot(["@vid", "@gif"])
# )
# async def _(_, m):
#     print(m)
#     await m.reply(str(m.media))

# @Client.on_poll(
# )
# async def _(_, p):
#     print(p)

# @Client.on_chat_member_updated()
# async def _(c, u):
#  await c.send_message(-1001220993104, str(u._raw), message_thread_id=1378275)
