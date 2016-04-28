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
# Timesamp: 4/28/16 :: 10:39 PM

from handler.irchandler import IrcHandler

class InvalidHandlerException(Exception):
    def __init__(self, handler):
        self.handler = handler

    def __str__(self):
        return "Invalide Handler {0} for dispatcher".format(self.handler)


class UnloadImpossibleException(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return "Command <{0}> couldn't be unloaded!".format(self.cmd)


class UnloadedHandlerException(Exception):
    def __init__(self, cmd):
        self.cmd = cmd

    def __str__(self):
        return "Command <{0}> isn't loaded!".format(self.cmd)


class Dispatcher(object):
    def __init__(self):
        super(Dispatcher, self).__init__()
        self.handlers = {}
        pass

    def is_valid_handler(self, handler):
        return isinstance(handler, IrcHandler)

    def register(self,handler):
        if not self.is_valid_handler(handler):
            raise InvalidHandler(handler)

        self.handlers[handler.name] = handler
        handler.notice_registration(self)

    def quit(self):
        for handler in self.handlers.values():
                handler.notice_unregistration(True)
        self.handlers.clear()

    def unregister(self,handlername):
        """
            Unload a module, this function can raise:
                UnloadImpossibleException
                UnloadedHandlerException
        """
        if handlername not in self.handlers:
            raise UnloadedHandlerException(handlername)

        self.handlers[handlername].notice_unregistration(False)
        del self.handlers[handlername]

    def can_access(self, msg):
        return True

    def dispatch(self, msg):
        for handler in self.handlers.values():
            match = handler.match(msg)
            if match and self.can_access(msg):
                handler.handle(match)
