#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pyrogram import Filters

from pyrobot import (
    SUDO_USERS
)


def f_sudo_filter(f, m):
    return bool(
        m.from_user.id in SUDO_USERS
    )


sudo_filter = Filters.create(
    func=f_sudo_filter,
    name="SudoFilter"
)