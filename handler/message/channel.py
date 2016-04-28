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
import crypt
from msghandler import PrivMsgHandler
from handler.command.command import CmdHandler

class ChannelMsgHandler(PrivMsgHandler):
    name = "channel"

    def match(self, *args):
        return False

    def handle(self, *args):
        raise NotImplemented

    def notice_registration(self, bot):
        super(ChannelMsgHandler, self).notice_registration(bot)
        self.sons = []
        self.raw_send = bot.s.send
        #Register interface
        bot.register_cmd(ChannelCmdHandler(self))

        self.sons.append(JoinCmdHandler(self, bot))
        self.sons.append(PartCmdHandler(self, bot))
        self.sons.append(QuitCmdHandler(self))
        for son in self.sons:
            bot.register_cmd(son)

    def notice_unregistration(self, quitting):
        super(ChannelMsgHandler, self).notice_unregistration(quitting)
        for son in self.sons:
            son.self_unload()

#These modules need to directly speak to the server so they use daddy's raw_send


class ChannelCmdHandler(CmdHandler):
    """Channel commands (join/part/quit)"""
    name = "channel"
    noregister = True

    def __init__(self, dad):
        self.dad = dad

    def match(self, msg):
        return False

    def notice_unregistration(self, quitting):
        super(ChannelCmdHandler, self).notice_unregistration(quitting)
        self.dad.self_unload()



class JoinCmdHandler(CmdHandler):
    """Say to the bot to join a canal : !join <canal>"""
    name = "join"
    noregister = True
    access ={name : set(['admin'])}

    def __init__(self, dad, bot):
        super(JoinCmdHandler, self).__init__()
        self.regexp = re.compile(r"join$")
        self.raw_send = dad.raw_send
        self.bot = bot

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if not args:
            self.send("Need a canal to join")
            return
        if args[0] in self.bot.chans:
            return
        self.raw_send("JOIN {0}\r\n".format(args[0]))
        self.bot.chans.append(args[0])

class PartCmdHandler(CmdHandler):
    """Say to the bot to part a canal : !part <canal>"""
    name = "part"
    noregister = True
    access ={name : set(['admin'])}

    def __init__(self, dad, bot):
        super(PartCmdHandler, self).__init__()
        self.regexp = re.compile(r"part$")
        self.raw_send = dad.raw_send
        self.bot = bot

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if not args:
            self.send("Need a canal to part")
            return
        if not args[0] in self.bot.chans:
            return
        self.raw_send("PART {0}\r\n".format(args[0]))
        self.bot.chans.remove(args[0])

class QuitCmdHandler(CmdHandler):
    """Say to the bot to quit : !quit <message>"""
    name = "quit"
    noregister = True
    access ={name : set(['admin'])}

    def __init__(self, dad):
        super(QuitCmdHandler, self).__init__()
        self.regexp = re.compile(r"quit$")
        self.raw_send = dad.raw_send

    def handle(self, nick, dest, cmd, arg):
        if not arg:
            self.send("Need a message")
            return
        if len(arg) > 200:
            arg = arg[:200] + "\r\n"
        self.raw_send("QUIT {0}\r\n".format(arg))
