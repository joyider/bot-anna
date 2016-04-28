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
from dispatcher import Dispatcher, UnloadImpossibleException, UnloadedHandlerException, InvalidHandlerException 

class CmdMsgHandler(Dispatcher, PrivMsgHandler):
    name = "cmd_dispatch"
    noregister = True
    def __init__(self):
        super(CmdMsgHandler, self).__init__()
        self.regexp = re.compile( ":(?P<nick>[^!]*)!\S* PRIVMSG (?P<dest>\S*) :(?P<msg>.*)")
        self.command_template = re.compile("!(?P<cmd>\S*) ?(?P<args>.*)")

    # PrivMsgHandler
    def handle(self, match):
        nick = match.group('nick')
        dest = match.group('dest')
        msg = match.group('msg')
        cmd_match = self.command_template.match(match.group('msg'))

        if not dest.startswith("#"):
            dest = nick

        if cmd_match:
            cmd = cmd_match.group('cmd').lower()
            args = cmd_match.group('args')
            self.dispatch(nick, dest, cmd, args)

    def notice_unregistration(self, quitting):
        if not quitting:
            raise UnloadImpossibleException(self.name)
        self.quit() 

    # Dispatcher
    def is_valid_handler(self, handler):
        return isinstance(handler, CmdHandler)

    def can_access(self, nick, dest, cmd, args):
        return True

    def dispatch(self, nick, dest, cmd, args):
            for handler in self.handlers.values():
                if handler.match(cmd):
                    if not self.can_access(nick, dest, cmd, args):
                        self.send("You don't have access to that command !", dest)
                        return
                    def response_send(msg):
                        self.send(msg, dest)
                    handler.set_send(response_send)
                    handler.handle(nick, dest, cmd, args)
