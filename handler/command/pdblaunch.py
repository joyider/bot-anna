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
from command import CmdHandler

class PdbCmdHandler(CmdHandler):
    """This Command allow to run a pdb on the bot"""
    name = "pdb"
    access = {name : set(['admin'])}

    def __init__(self):
        super(PdbCmdHandler, self).__init__()
        self.regexp = re.compile(r"pdb$")

    def notice_registration(self, cmd_dispatcher):
        super(PdbCmdHandler, self).notice_registration(cmd_dispatcher)
        self.dispatcher = cmd_dispatcher


    def handle(self, nick, dest, cmd, arg):
        self.send("Launch Pdb")
        import pdb; pdb.set_trace()
