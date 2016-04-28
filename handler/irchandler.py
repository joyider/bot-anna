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
# Timesamp: 4/28/16 :: 10:43 PM

import re

class NotImplementedHandler(Exception):
    pass

class IrcHandler(object):
    name = ""
    def __init__(self):
        super(IrcHandler, self).__init__()
        self.regexp = re.compile("")
        self.send = self.default_send


    def match(self, msg):
        return self.regexp.match(msg)

    def handle(self, match):
        raise NotImplementedHandler("Handle method not implemented for {0}".format(type(self)))

    def notice_registration(self, bot):
        self.set_send(bot.send_msg)
        self.self_unload = lambda : bot.unregister(self.name)

    def notice_unregistration(self, quitting):
        self.self_unload = lambda : None

    def default_send(self, *args):
        raise NotImplementedHandler("This handler {0} is not registered to a bot".format(self))

    def set_send(self, send_methode):
        self.send  = send_methode
