#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K


import os

from pyrobot import TMP_DOWNLOAD_DIRECTORY


def is_thumb_image_exists():
    thumb_image_path = TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    if os.path.exists(thumb_image_path):
        thumb_image_path = TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    else:
        thumb_image_path = None
    return thumb_image_path
