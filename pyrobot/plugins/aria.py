"""A Torrent Client Plugin Based On Aria2 for Userbot
Source: https://github.com/SpEcHiDe/UniBorg/blob/master/stdplugins/aria_two.py by @Zero_cool7870

   Magnet link: .addmag 
   Torrent file from local: .addtor
   Remove All Downloads: .ariaRM
   Pause All Downloads: .ariaP
   Resume All Downloads: .ariaR
   Show Downloads: .ariastatus

@user_nmr
"""

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import aria2p
import asyncio
import io
import os
from pyrobot import COMMAND_HAND_LER
from pyrogram import Client, Filters

cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true --allow-overwrite=true"
EDIT_SLEEP_TIME_OUT = 6
aria2_is_running = os.system(cmd)
aria2 = aria2p.API(
		aria2p.Client(
			host="http://localhost",
			port=6800,
			secret=""
		)
	)

@Client.on_message(Filters.command("addmag", COMMAND_HAND_LER)  & Filters.me)
async def magnet_download(client, event):
	var = event.text
	var = var[8:]	
	magnet_uri = var
	magnet_uri = magnet_uri.replace("`","")
	logger.info(magnet_uri)
	try: #Add Magnet URI Into Queue
		download = aria2.add_magnet(magnet_uri)
	except Exception as e:
		logger.info(str(e))
		await event.edit("Error :\n{}".format(str(e)))
		return
	gid = download.gid
	await progress_status(gid=gid,event=event,previous=None)
	await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
	new_gid = await check_metadata(gid)
	await progress_status(gid=new_gid,event=event,previous=None)
	
@Client.on_message(Filters.command("addtor", COMMAND_HAND_LER)  & Filters.me)
async def torrent_download(client, event):
	var = event.text[8:]
	torrent_file_path = var	
	torrent_file_path = torrent_file_path.replace("`","")
	logger.info(torrent_file_path)

	try: #Add Torrent Into Queue
		download = aria2.add_torrent(torrent_file_path, uris=None, options=None, position=None)
	except Exception as e:
		await event.edit("Error :\n`{}`".format(str(e)))
		return
	gid = download.gid
	await progress_status(gid=gid,event=event,previous=None)

@Client.on_message(Filters.command("ariaRM", COMMAND_HAND_LER)  & Filters.me)
async def remove_all(client, event):
	try:
		removed = aria2.remove_all(force=True)
		aria2.purge_all()
	except:
		pass
	if removed == False:  #If API returns False Try to Remove Through System Call.
		os.system("aria2p remove-all")
	await event.edit("`Removed All Downloads.`")  

@Client.on_message(Filters.command("ariaP", COMMAND_HAND_LER)  & Filters.me)
async def pause_all(client, event):
    # Pause ALL Currently Running Downloads.
    paused = aria2.pause_all(force=True)
    await event.edit("Output: " + str(paused))

@Client.on_message(Filters.command("ariaR", COMMAND_HAND_LER)  & Filters.me)
async def resume_all(client, event):
    resumed = aria2.resume_all()
    await event.edit("Output: " + str(resumed))

@Client.on_message(Filters.command("ariastatus", COMMAND_HAND_LER)  & Filters.me)
async def show_all(client, event):
	output = "output.txt"
	downloads = aria2.get_downloads() 
	msg = ""
	for download in downloads:
		msg = msg+"File: `"+str(download.name) +"`\nSpeed: "+ str(download.download_speed_string())+"\nProgress: "+str(download.progress_string())+"\nTotal Size: "+str(download.total_length_string())+"\nStatus: "+str(download.status)+"\nETA:  "+str(download.eta_string())+"\n\n"
	if len(msg) <= 4096:
		await event.edit("`Current Downloads: `\n"+msg)
	else:
		await event.edit("`Output is huge.Sending as file.. `")
		with open(output,'w') as f:
			f.write(msg)
		await asyncio.sleep(2)	
		await event.delete()	
		await client.send_document(
			chat_id=event.chat_id,
			document=output,
			caption="`Output is huge. Sending as a file...`", 
			)				

async def check_metadata(gid):
	file = aria2.get_download(gid)
	new_gid = file.followed_by_ids[0]
	logger.info("Changing GID "+gid+" to "+new_gid)
	return new_gid	

async def progress_status(gid,event,previous):
	try:
		file = aria2.get_download(gid)
		if not file.is_complete:
			if not file.error_message:
				msg = "Downloading File: `"+str(file.name) +"`\nSpeed: "+ str(file.download_speed_string())+"\nProgress: "+str(file.progress_string())+"\nTotal Size: "+str(file.total_length_string())+"\nStatus: "+str(file.status)+"\nETA:  "+str(file.eta_string())+"\n\n"
				if previous != msg:
					await event.edit(msg)
					previous = msg
			else:
				logger.info(str(file.error_message))
				await event.edit("Error : `{}`".format(str(file.error_message)))		
				retur
			await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
			await progress_status(gid,event,previous)
		else:
			await event.edit("File Downloaded Successfully: `{}`".format(file.name))
			return
	except Exception as e:
		if " not found" in str(e) or "'file'" in str(e):
			await event.edit("Download Canceled :\n`{}`".format(file.name))
			return
		elif " depth exceeded" in str(e):
			file.remove(force=True)
			await event.edit("Download Auto Canceled :\n`{}`\nYour Torrent/Link is Dead.".format(file.name))
		else:
			logger.info(str(e))
			await event.edit("Error :\n`{}`".format(str(e)))
			return
