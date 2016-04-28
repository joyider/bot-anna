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
from handler.irchandler import IrcHandler

class NotImplementedCmdHandler(Exception):
    pass

class CmdHandler(IrcHandler):

    def handle(self, nick, dest, cmd, arg):
        raise NotImplementedCmdHandler("command handle not implemented")

    def notice_registration(self, cmd_dispatcher):
        self.self_unload = lambda : cmd_dispatcher.unregister(self.name)

    def notice_unregistration(self, quitting):
        self.self_unload = lambda : None



class TestCmdHandler(CmdHandler):
    name = "test"

    def __init__(self):
        super(TestCmdHandler, self).__init__()
        self.regexp = re.compile(r"test$")

    def handle(self,nick, dest, cmd, arg):
        self.send("TEST WITH ARG:{0}".format(arg))


class QuitCmdHandler(CmdHandler):
    name = "bye"

    def __init__(self):
        super(EvalCmdHandler, self).__init__()
        self.regexp = re.compile(r"({[Q]uit|[dD]eco|[bB]ye)")

    def handle(self, nick, dest, cmd, arg):
        self.send("Bye !")
        exit()
