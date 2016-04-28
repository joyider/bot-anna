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


class MsgHandler(IrcHandler):
    pass


class PrivMsgHandler(MsgHandler):
    Priv_Regexp = ":(?P<nick>[^!]*)!\S* PRIVMSG (?P<dest>\S*) :"
    def set_send(self, send_method):
        def send_privmsg(msg, dest):
            send_method("PRIVMSG {0} :{1}\r\n".format(dest, msg))
        self.send = send_privmsg
