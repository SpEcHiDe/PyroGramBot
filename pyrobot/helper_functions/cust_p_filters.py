#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyrogram import (
    filters
)
from pyrobot import (
    SUDO_USERS,
    USE_AS_BOT
)
from pyrobot.helper_functions.admin_check import admin_check


def f_sudo_filter(filt, client, message):
    return bool(
        (
            (
                message.from_user and
                message.from_user.id in SUDO_USERS
            ) or
            (
                message.sender_chat and
                message.sender_chat.id in SUDO_USERS
            )
        ) and
        # t, lt, fl 2013
        not message.edit_date
    )


sudo_filter = filters.create(
    func=f_sudo_filter,
    name="SudoFilter"
)


def onw_filter(filt, client, message):
    if USE_AS_BOT:
        return bool(
            True and # message.from_user.id in SUDO_USERS
            # t, lt, fl 2013
            not message.edit_date
        )
    else:
        return bool(
            message.from_user and
            message.from_user.is_self and
            # t, lt, fl 2013
            not message.edit_date
        )


f_onw_fliter = filters.create(
    func=onw_filter,
    name="OnwFilter"
)


async def admin_filter_f(filt, client, message):
    return (
        # t, lt, fl 2013
        not message.edit_date and
        await admin_check(message)
    )


admin_fliter = filters.create(
    func=admin_filter_f,
    name="AdminFilter"
)
