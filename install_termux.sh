#!/bin/sh
# -*- coding: utf-8 -*-

# the entire source code is GPL, except this file,
# which is AGPL
# (c) 2017

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# the below two lines were taken without
# permission from 
# https://github.com/friendly-telegram/friendly-telegram/blob/master/install.sh#L62
if [ "$OSTYPE" = "linux-android" ]; then
  pkg install -y python git || { echo "installation of Python and GiT failed"; exit 2; }
  # the above lines were taken without 
  # permission from 
  # https://github.com/friendly-telegram/friendly-telegram/blob/master/install.sh#L62
  # create a virtual environment
  python3.7 -m venv venv
  . ./venv/bin/activate
  mkdir -p /sdcard/Telegram
  # create and change into accessible sub directory
  cd /sdcard/Telegram
  # install async
  pip install https://github.com/pyrogram/pyrogram/archive/asyncio.zip
  git clone https://github.com/SpEcHiDe/PyroGramUserBot
  cd PyroGramUserBot
  # generate string session
  python3 GenerateStringSession.py
  cd ..
  # cleanup
  rm -rf PyroGramUserBot
fi
