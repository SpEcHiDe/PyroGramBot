#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
import json
import os
import shutil

from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import (
    InputMediaDocument,
    InputMediaVideo,
    InputMediaAudio
)

from pyrobot import (
    LOGGER,
    TMP_DOWNLOAD_DIRECTORY
)
from pyrobot.helper_functions.check_if_thumb_exists import is_thumb_image_exists
from pyrobot.helper_functions.display_progress_dl_up import progress_for_pyrogram
from pyrobot.helper_functions.run_shell_cmnd import run_command


async def youtube_dl_call_back(bot, update, cb_data):
    LOGGER.info(update)
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    #
    current_user_id = update.message.reply_to_message.from_user.id
    current_touched_user_id = update.from_user.id
    if current_user_id != current_touched_user_id:
        return False, None
    user_working_dir = os.path.join(TMP_DOWNLOAD_DIRECTORY, str(current_user_id))
    # create download directory, if not exist
    if not os.path.isdir(user_working_dir):
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=[
                update.message.message_id,
                update.message.reply_to_message.message_id,
            ],
            revoke=True
        )
        return
    save_ytdl_json_path = user_working_dir + \
        "/" + str("ytdleech") + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f_d:
            response_json = json.load(f_d)
        os.remove(save_ytdl_json_path)
    except FileNotFoundError:
        await bot.delete_messages(
            chat_id=update.message.chat.id,
            message_ids=[
                update.message.message_id,
                update.message.reply_to_message.message_id,
            ],
            revoke=True
        )
        return False
    #
    response_json = response_json[0]
    # TODO: temporary limitations
    LOGGER.info(response_json)
    #
    youtube_dl_url = response_json.get("webpage_url")
    LOGGER.info(youtube_dl_url)
    #
    custom_file_name = "%(title)s.%(ext)s"
    # https://superuser.com/a/994060
    LOGGER.info(custom_file_name)
    #
    await update.message.edit_caption(
        caption="trying to download"
    )
    description = "@PyroGramBot"
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]
        # escape Markdown and special characters
    #
    tmp_directory_for_each_user = os.path.join(
        TMP_DOWNLOAD_DIRECTORY,
        str(update.from_user.id)
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user
    download_directory = os.path.join(tmp_directory_for_each_user, custom_file_name)
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "youtube-dl",
            "-c",
            "--prefer-ffmpeg",
            "--extract-audio",
            "--add-metadata",
            "--embed-thumbnail",
            "--audio-format", youtube_dl_ext,
            "--audio-quality", youtube_dl_format,
            youtube_dl_url,
            "-o", download_directory,
            # "--external-downloader", "aria2c"
        ]
    else:
        # command_to_exec = ["youtube-dl", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            for for_mat in response_json["formats"]:
                format_id = for_mat.get("format_id")
                if format_id == youtube_dl_format:
                    acodec = for_mat.get("acodec")
                    vcodec = for_mat.get("vcodec")
                    if acodec == "none" or vcodec == "none":
                        minus_f_format = youtube_dl_format + "+bestaudio"
                    break
        command_to_exec = [
            "youtube-dl",
            "-c",
            # "--embed-subs",
            "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory,
            # "--external-downloader", "aria2c"
        ]
    #
    command_to_exec.append("--no-warnings")
    # command_to_exec.append("--quiet")
    command_to_exec.append("--restrict-filenames")
    #
    if "hotstar" in youtube_dl_url:
        command_to_exec.append("--geo-bypass-country")
        command_to_exec.append("IN")
    LOGGER.info(command_to_exec)
    start = datetime.now()    
    t_response, e_response = await run_command(command_to_exec)
    # LOGGER.info(e_response)
    # LOGGER.info(t_response)
    ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await update.message.edit_caption(
            caption=error_message
        )
        return False, None
    if t_response:
        # LOGGER.info(t_response)
        # os.remove(save_ytdl_json_path)
        end_one = datetime.now()
        time_taken_for_download = (end_one -start).seconds
        dir_contents = os.listdir(tmp_directory_for_each_user)
        # dir_contents.sort()
        await update.message.edit_caption(
            f"found {len(dir_contents)} files"
            f"\n Download took {time_taken_for_download} seconds"
            "\n Trying to Upload, now ..."
        )
        LOGGER.info(dir_contents)
        #
        for single_file in dir_contents:
            local_file_name = os.path.join(tmp_directory_for_each_user, single_file)
            thumb = await is_thumb_image_exists(local_file_name)
            caption_str = os.path.basename(local_file_name)
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            artist = ""
            title = ""
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            width, height = 0, 0
            if thumb is not None:
                metadata = extractMetadata(createParser(thumb))
                if metadata.has("height"):
                    height = metadata.get("height")
                if metadata.has("width"):
                    height = metadata.get("width")
            if local_file_name.upper().endswith(("MKV", "MP4", "WEBM")):
                await update.message.edit_media(
                    media=InputMediaVideo(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        width=width,
                        height=height,
                        duration=duration,
                        supports_streaming=True
                    )
                )
            elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV")):
                await update.message.edit_media(
                    media=InputMediaAudio(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        duration=duration,
                        performer=artist,
                        title=title
                    )
                    # quote=True,
                )
            else:
                await update.message.edit_media(
                    media=InputMediaDocument(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html"
                    )
                    # quote=True,
                )
        #
        try:
            shutil.rmtree(tmp_directory_for_each_user)
        except:
            pass
        #
