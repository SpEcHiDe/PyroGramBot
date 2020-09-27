#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K


import asyncio
import aiohttp
import json
import os
from PIL import Image
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrobot.helper_functions.display_progress_dl_up import humanbytes
from pyrobot import (
    LOGGER
)


async def proc_ess_image_aqon(image_url: str, output_dir: str) -> str:
    async with aiohttp.ClientSession() as session:
        noqa_read = await session.get(image_url)
        image_content = await noqa_read.read()
        thumb_img_path = os.path.join(
            output_dir,
            "thumb_image.jpg"
        )
        with open(thumb_img_path, "wb") as f_d:
            f_d.write(image_content)
    # image might be downloaded in the previous step
    # https://stackoverflow.com/a/21669827/4723940
    Image.open(thumb_img_path).convert(
        "RGB"
    ).save(thumb_img_path, "JPEG")
    # ref: https://t.me/PyrogramChat/44663
    # return the downloaded image path
    return thumb_img_path


async def extract_youtube_dl_formats(url, user_working_dir):
    command_to_exec = [
        "youtube-dl",
        "--no-warnings",
        "--youtube-skip-dash-manifest",
        "-j",
        url
    ]
    if "hotstar" in url:
        command_to_exec.append("--geo-bypass-country")
        command_to_exec.append("IN")
    LOGGER.info(command_to_exec)
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    LOGGER.info(e_response)
    t_response = stdout.decode().strip()
    LOGGER.info(t_response)
    # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
    if e_response:
        # logger.warn("Status : FAIL", exc.returncode, exc.output)
        error_message = e_response.replace(
            (
                "please report this issue on https://yt-dl.org/bug . "
                "Make sure you are using the latest version; see  "
                "https://yt-dl.org/update  on how to update. "
                "Be sure to call youtube-dl with the --verbose flag and "
                "include its complete output."
            ), ""
        )
        return None, error_message, None
    if t_response:
        # logger.info(t_response)
        x_reponse = t_response
        response_json = []
        if "\n" in x_reponse:
            for yu_r in x_reponse.split("\n"):
                response_json.append(json.loads(yu_r))
        else:
            response_json.append(json.loads(x_reponse))
        # response_json = json.loads(x_reponse)
        save_ytdl_json_path = user_working_dir + \
            "/" + str("ytdleech") + ".json"
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        # logger.info(response_json)
        inline_keyboard = []
        #
        thumb_image = "https://placehold.it/90x90"
        #
        for current_r_json in response_json:
            #
            thumb_image = current_r_json.get("thumbnail", thumb_image)
            #
            duration = None
            if "duration" in current_r_json:
                duration = current_r_json["duration"]
            if "formats" in current_r_json:
                for formats in current_r_json["formats"]:
                    format_id = formats.get("format_id")
                    format_string = formats.get("format_note")
                    if format_string is None:
                        format_string = formats.get("format")
                    format_ext = formats.get("ext")
                    approx_file_size = ""
                    if "filesize" in formats:
                        approx_file_size = humanbytes(formats["filesize"])
                    dipslay_str_uon = (
                        f" {format_string} ({format_ext.upper()}) "
                        f"{approx_file_size} "
                    )
                    cb_string_video = f"ytdl_video|{format_id}|{format_ext}"
                    ikeyboard = []
                    if "drive.google.com" in url:
                        if format_id == "source":
                            ikeyboard = [
                                InlineKeyboardButton(
                                    dipslay_str_uon,
                                    callback_data=cb_string_video
                                )
                            ]
                    else:
                        if format_string and "audio only" not in format_string:
                            ikeyboard = [
                                InlineKeyboardButton(
                                    dipslay_str_uon,
                                    callback_data=cb_string_video
                                )
                            ]
                        else:
                            # special weird case :\
                            ikeyboard = [
                                InlineKeyboardButton(
                                    f"SVideo [] ( {approx_file_size} )",
                                    callback_data=cb_string_video
                                )
                            ]
                    inline_keyboard.append(ikeyboard)
                if duration is not None:
                    cb_string_64 = "ytdl_audio|64k|MP3"
                    cb_string_128 = "ytdl_audio|128k|MP3"
                    cb_string = "ytdl_audio|320k|MP3"
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "MP3 (64 kbps)",
                            callback_data=cb_string_64
                        ),
                        InlineKeyboardButton(
                            "MP3 (128 kbps)",
                            callback_data=cb_string_128
                        )
                    ])
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "MP3 (320 kbps)",
                            callback_data=cb_string
                        )
                    ])
            else:
                format_id = current_r_json["format_id"]
                format_ext = current_r_json["ext"]
                cb_string_video = f"ytdl_video|{format_id}|{format_ext}"
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "SVideo",
                        callback_data=cb_string_video
                    )
                ])
            break
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        # YouTubeDL hot-patching: #397
        thumb_image = await proc_ess_image_aqon(
            thumb_image,
            user_working_dir
        )
        # LOGGER.info(reply_markup)
        succss_mesg = "Select the desired format: 👇\n"
        succss_mesg += "<u>mentioned</u> <i>file size might be approximate</i>"
        return thumb_image, succss_mesg, reply_markup
