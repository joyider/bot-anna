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
from msghandler import PrivMsgHandler
from handler.command.command import CmdHandler


class FuckMsgHandler(PrivMsgHandler):
    name = "fuck"
    def __init__(self):
        super(FuckMsgHandler, self).__init__()
        self.regexp = re.compile(self.Priv_Regexp + "\s*(?P<fuck>fuck(ing)?) \s*(?P<tofuck>.*)")

    def notice_registration(self, bot):
        super(FuckMsgHandler, self).notice_registration(bot)
        bot.register_cmd(FuckCmdHandler(self))

    def handle(self, match):
        to_fuck = match.group('tofuck')
        dest = match.group('dest')
        if not dest.startswith("#"):
            return

        if not to_fuck:
            return

        if match.group('fuck') == 'fuck':
            self.send("YEAH FUCK " + to_fuck.strip().upper(), match.group("dest"))
        else:
            self.send("YEAH FUCKING " + to_fuck.strip().upper(), match.group("dest"))

class FuckCmdHandler(CmdHandler):
    """Fuck it"""
    name = "fuck"

    def __init__(self, dad):
        self.dad = dad

    def match(self, msg):
        return False

    def notice_unregistration(self, quitting):
        self.dad.self_unload()
