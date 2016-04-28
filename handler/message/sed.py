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


class SedMsgHandler(PrivMsgHandler):
    name = "sed"
    def __init__(self):
        super(SedMsgHandler, self).__init__()
        self.regexp = re.compile(self.Priv_Regexp + "\s*:?s(?P<sep>[/%=_])(?P<sed_regexp>.*?)(?P=sep)(?P<replace>.*?)(?P=sep).*")
        self.msg_reg = re.compile(self.Priv_Regexp + "(?P<msg>.*)")
        self.last_log = {}

    def notice_registration(self, bot):
        super(SedMsgHandler, self).notice_registration(bot)
        bot.register_cmd(SedCmdHandler(self)) 

    #Need to register all last phrase from users
    def match(self, msg):
        match =  self.msg_reg.match(msg)
        match_sed = self.regexp.match(msg)
        if match and not match_sed:
            nick = match.group('nick')
            dest = match.group('dest')
            msg = match.group('msg')
            if not dest.startswith("#"):
                return False
            if dest not in self.last_log:
                self.last_log[dest] = {}
            self.last_log[dest][nick] = msg

        return match_sed

    def handle(self, match):
        dest = match.group('dest')
        if not dest.startswith("#"):
            return
        nick = match.group('nick')
        sed_regexp = match.group('sed_regexp')
        replace = match.group('replace')

        if (dest not in self.last_log or
            nick not in self.last_log[dest]):
            self.send("Nothing to correct", dest)
            return

        msg = self.last_log[dest][nick]
        try:
            self.send("<{0}>: ".format(nick) +re.sub(sed_regexp, replace, msg), dest)
        except:
            self.send("Invalid regexp : {0}".format(sed_regexp), dest)


class SedCmdHandler(CmdHandler):
    """Sed autocorrection (s/pyregexp/replacement/)"""
    name = "sed"
  
    def __init__(self, dad):
        self.dad = dad
 
    def match(self, msg):
        return False 

    def notice_unregistration(self, quitting):
        self.dad.self_unload()
