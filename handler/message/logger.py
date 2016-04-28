#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# bot-anna (c) 2016 by Andre Karlsson<andre.karlsson@protractus.se>
#
# This file is part of bot-anna.
#
#    bot-anna is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Filename:  by: andrek
# Timesamp: 4/28/16 :: 10:38 PM

import re
import datetime
import time
from os import mkdir, path

from msghandler import PrivMsgHandler
from handler.command.command import CmdHandler



class LogMsgHandler(PrivMsgHandler):
    name = "log"
    def __init__(self):
        super(LogMsgHandler, self).__init__()
        self.regexp = re.compile( self.Priv_Regexp +  "(?P<msg>.*)")
        self.folder_format = "%d-%m-%y"
        self.dir_base = 'logs/'
        self.logday = datetime.date.today()
        self.log_folder = self.logday.strftime(self.folder_format)

        if not path.exists(self.dir_base):
            mkdir(self.dir_base)
        if not path.exists(self.dir_base + self.log_folder):
            mkdir(self.dir_base + self.log_folder)

    def notice_registration(self, bot):
        super(LogMsgHandler, self).notice_registration(bot)
        bot.register_cmd(LogCmdHandler(self))
        self.bot_nick = bot.nick

    def handle(self, match):
        nick = match.group('nick')
        dest = match.group('dest')
        msg = match.group('msg').strip()

        today = datetime.date.today()
        if self.logday != today:
            self.logday = today
            self.log_folder = self.logday.strftime(self.folder_format)
            if not path.exists(self.dir_base + self.log_folder):
                mkdir(self.dir_base + self.log_folder)

        if not dest.startswith('#'):
            dest = nick

        f = open(self.dir_base +  self.log_folder + '/' + dest, 'a+')
        strnow = time.strftime("%H:%M:%S")
        f.write("{0} <{1}>: {2}\n".format(strnow, nick, msg))
        f.close()


class LogCmdHandler(CmdHandler):
    """Log Module"""
    name = "log"

    def __init__(self, dad):
        self.dad = dad

    def match(self, msg):
        return False

    def notice_unregistration(self, quitting):
        self.dad.self_unload()
