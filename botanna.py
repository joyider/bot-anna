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
# Timesamp: 4/28/16 :: 10:40 PM

import sys
import socket
import ssl
import string
import time

from handler import *
from config import *
from dispatcher import Dispatcher

class IrcBot(Dispatcher):
    def __init__(self, nick, ident, realn):
        super(IrcBot, self).__init__()
        self.nick = nick
        self.ident = ident
        self.realn= realn
        self.s = socket.socket()
        self.chans = []

        self.def_cmd_dispatch = msg_handlers['cmd_dispatch']()
        self.register(self.def_cmd_dispatch)

    def connect(self, (HOST, PORT), enable_ssl=False):
        if enable_ssl:
            self.s = ssl.wrap_socket(self.s)
        self.s.connect((HOST, PORT))
        self.s.send("NICK %s\r\n" % self.nick)
        self.s.send("USER %s %s bla :%s\r\n" % (self.ident, HOST, self.realn))


    def join(self, chan):
        self.chans.append(chan)

    def send_msg(self, msg):
        if len(msg) > 200:
            self.s.send(msg[:200] + "\r\n")
        else:
            self.s.send(msg)

    def register_cmd(self, cmdhandler):
        self.def_cmd_dispatch.register(cmdhandler)

    def launch(self):
        try:
            self.s.recv(42000)
            for chan in self.chans:
                self.s.send("JOIN {0}\r\n".format(chan))
            data = "DATA"
            while data:
                data = self.s.recv(4096)
                if data:
                    self.dispatch(data)
        finally:
          # We unregister (unload) every CmdHandler to quit properly
          self.quit()
          self.s.send("QUIT Quit.\r\n")


tbot = IrcBot(NICK, IDENT, REALNAME)
tbot.connect((HOST,PORT), IS_SSL)

for msg_name in msg_handlers:
    if not hasattr(msg_handlers[msg_name], "noregister"):
        print "load {0}".format(msg_name)
        tbot.register(msg_handlers[msg_name]())
        pass

for cmd_name in cmd_handlers:
    if not hasattr(cmd_handlers[cmd_name], "noregister"):
        print "load {0}".format(cmd_name)
        tbot.register_cmd(cmd_handlers[cmd_name]())
        pass

tbot.register_cmd(cmd_handlers['auth'](PASSWORD))
tbot.register_cmd(cmd_handlers['events']('http://178.170.99.117/ircbot/', '/data/www/ircbot'))

print "Bot lanched !"

tbot.join("#mytest")
#tbot.join("#tocard-stage")
tbot.launch()
