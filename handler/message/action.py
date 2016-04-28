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

class ActionMsgHandler(PrivMsgHandler):
      name = "action"
      def __init__(self):
          pass

      def match(self, *args):
          return False

      def handle(self, *args):
          raise NotImplemented

      def notice_registration(self, bot):
          super(ActionMsgHandler, self).notice_registration(bot)
          self.raw_send = bot.s.send
          bot.register_cmd(ActionCmdHandler(self, bot))

      def notice_unregistration(self, quitting):
          super(ActionMsgHandler, self).notice_unregistration(quitting)

class ActionCmdHandler(CmdHandler):
    """Action command: !action #chan <msg>"""
    name = "action"
    access = {name: set(['admin'])}

    def __init__(self, dad, bot):
        self.regexp = re.compile(r"action$")
        self.dad = dad
        self.bot = bot

    def handle(self, nick, dest, cmd, arg):
        args = arg.split(None, 1)
        if len(args) != 2:
            self.send("This command needs at least two arguments.")
            return
        if not args[0] in self.bot.chans:
            self.send("I am not on canal {0}. You may want to join it first".format(args[0]))
            return
        self.dad.raw_send("PRIVMSG {0} :\001ACTION {1}\001\r\n".format(args[0], args[1]))

    def notice_unregistration(self, quitting):
        self.dad.notice_unregistration(quitting)
