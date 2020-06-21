#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyrogram import (
    Filters,
    Message
)

from pyrobot import (
    SUDO_USERS,
    USE_AS_BOT
)


def f_sudo_filter(f, m: Message):
    return bool(
        m.from_user.id in SUDO_USERS
    )


sudo_filter = Filters.create(
    func=f_sudo_filter,
    name="SudoFilter"
)

def onw_filter(f, m: Message):
    if USE_AS_BOT:
        return bool(
            m.from_user.id in SUDO_USERS
        )
    else:
        return bool(
            m.from_user and 
            m.from_user.is_self
        )


f_onw_fliter = Filters.create(
    func=onw_filter,
    name="OnwFilter"
)
