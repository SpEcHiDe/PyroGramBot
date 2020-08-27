#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyrogram import (
    filters
)
from pyrobot import (
    SUDO_USERS,
    USE_AS_BOT
)


def f_sudo_filter(filt, client, message):
    return bool(
        message.from_user.id in SUDO_USERS
    )


sudo_filter = filters.create(
    func=f_sudo_filter,
    name="SudoFilter"
)

def onw_filter(filt, client, message):
    if USE_AS_BOT:
        return bool(
            message.from_user.id in SUDO_USERS
        )
    else:
        return bool(
            message.from_user and 
            message.from_user.is_self
        )


f_onw_fliter = filters.create(
    func=onw_filter,
    name="OnwFilter"
)
