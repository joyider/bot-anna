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

import handler

from msghandler import PrivMsgHandler
from handler.command.command import CmdHandler
from dispatcher import UnloadImpossibleException, UnloadedHandlerException

class LoadMsgHandler(PrivMsgHandler):
    name = "load"
    def match(self, msg):
        return False

    def notice_registration(self, bot):
        super(LoadMsgHandler, self).notice_registration(bot)
        self.sons = []
        self.bot = bot
        #Register interface
        bot.register_cmd(LoadInterface(self))
        bot.register_cmd(LoadCmdHandler(self))

        bot.register_cmd(UnloadCmdHandler())

    def notice_unregistration(self, quitting):
        super(LoadMsgHandler, self).notice_unregistration(quitting)

    def load_module(self, mod):
        self.bot.register(mod)


class LoadInterface(CmdHandler):
    """ Load module"""
    name = "load-mod"
    def __init__(self, dad):
        self.dad = dad

    def match(self, msg):
        return False

    def notice_unregistration(self, quitting):
        super(LoadInterface, self).notice_unregistration(quitting)
        self.dad.self_unload()


class LoadCmdHandler(CmdHandler):
    """load command: !load <cmd>"""
    name = "load"
    access = {name : set(['admin'])}

    def __init__(self, dad):
        super(LoadCmdHandler, self).__init__()
        self.regexp = re.compile("(re)?load" + "$")
        self.dad = dad

    def notice_registration(self, cmd_dispatcher):
        self.cmd_dispatcher = cmd_dispatcher

    def notice_unregistration(self, quitting):
        if not quitting:
            raise UnloadImpossibleException(self.name)

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if not args:
            self.send("This command needs an argument.")
            return

        hdlr = args[0]
        if handler.reload_command(hdlr):
            handl = handler.cmd_handlers[hdlr]()
            self.hook_handler(handl)
            self.cmd_dispatcher.register(handl)
            self.send("cmd <{0}> loaded".format(hdlr))
            return
        if handler.reload_message(hdlr):
            handl = handler.msg_handlers[hdlr]()
            self.hook_handler(handl)
            self.dad.bot.register(handl)
            self.send("module <{0}> loaded".format(hdlr))
            return
        else:
            self.send("Unknow name <{0}>".format(hdlr))

    def hook_handler(self, handler):
        old_match = handler.match
        old_handle = handler.handle
        def hook_match(*msg):
            try:
                return old_match(*msg)
            except Exception as e:
                self.send("Error in module {0} : unloaded".format(handler.name))
                self.send(e)
                self.cmd_dispatcher.unregister(handler.name)

        def hook_handle(*args):
            try:
                return old_handle(*args)
            except Exception as e:
                self.send("Error in module {0} : unloaded".format(handler.name))
                self.send(e)
                self.cmd_dispatcher.unregister(handler.name)

        handler.match = hook_match
        handler.handle = hook_handle


class UnloadCmdHandler(CmdHandler):
    """Unload a loaded command: !unload <cmd>"""
    name = "unload"
    access = {name : set(['admin'])}

    def __init__(self):
        super(UnloadCmdHandler, self).__init__()
        self.regexp = re.compile(r"unload$")

    def notice_registration(self, cmd_dispatcher):
        self.cmd_dispatcher = cmd_dispatcher

    def notice_unregistration(self, quitting):
        if not quitting:
            raise UnloadImpossibleException(self.name)

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if not args:
            self.send("This command needs an argument.")
            return
        try:
            self.cmd_dispatcher.unregister(args[0])
            self.send("Command <{0}> succesfully unloaded!".format(args[0]))
        except UnloadImpossibleException as e:
            self.send(e)
        except UnloadedHandlerException as e:
            self.send(e)
