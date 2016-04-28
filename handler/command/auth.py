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
from command import CmdHandler
from dispatcher import UnloadImpossibleException

class AuthCmdHandler(CmdHandler):
    """This command handle authentification and exec rights for commands"""
    name = "auth"
    noregister = True

    def __init__(self, passwd='bite'):
        super(AuthCmdHandler, self).__init__()
        self.regexp = re.compile(r"auth$")
        self.access = {'auth' : set(['all'])}
        self.passwd = passwd
        self.connected = set(['hakril'])

        self.subcommand = {'connect' : self.connect, 'allow' : self.add_access,
                   'forbid' : self.rm_access, 'show' : self.show_access,
                    'connected': self.show_connected}


    def register(self, cmdhandler):
        if not hasattr(cmdhandler, "access"):
            return
        self.access.update(cmdhandler.access)

    def hook_register(self, cmdhandler):
        register_origin = cmdhandler.register
        def new_register(cmdhandler):
            self.register(cmdhandler)
            register_origin(cmdhandler)
        return new_register

    def notice_registration(self, cmdhandler):
        super(AuthCmdHandler, self).notice_registration(cmdhandler)
        cmdhandler.can_access = self.can_access
        #register pre registered commands
        for cmd in cmdhandler.handlers.values():
            self.register(cmd)
        #add hook for post registered command
        cmdhandler.register = self.hook_register(cmdhandler)

    def notice_unregistration(self, quitting):
        if not quitting:
            raise UnloadImpossibleException(self.name)

    def can_access(self, nick, dest, cmd, arg):
        cmd = cmd.lower()

        if cmd not in self.access:
            return False

        if 'all' in self.access[cmd]:
            return True

        if nick in self.connected and 'admin' in self.access[cmd]:
            return True

        if nick in self.access[cmd]:
            return True

        #Last hope if auth was forbid for all
        if nick in self.connected and cmd == 'auth':
            return True

        return False

    def handle(self, nick , dest, cmd, arg):
        args = arg.split()
        if len(args) < 1:
            self.send("Missing arg")
            return
        if args[0] in self.subcommand:
            self.subcommand[args[0]](nick, args)
        else:
            self.send("Unknow subcommand: {0}".format(args[0]))

    def connect(self, nick, args):
        return
        if len(args) < 2:
            self.send("!auth connect passwd")
            return
        if args[1] == self.passwd:
            self.connected.add(nick)
            self.send("{0} is now connected !".format(nick))
            return
        self.send("Bad passwd sorry")

    def add_access(self, nick, args):
        if len(args) < 2:
            self.send("!auth allow cmd nick")
            return

        dest_nick = nick
        if len(args) == 3:
            dest_nick = args[2]
             
        if nick not in self.connected:
            self.send("You can't do that : connect before")
            return
        if args[1] not in self.access:
            self.access[args[1]] = set()
        self.access[args[1]].add(dest_nick)
        self.send("{0} can now use {1}".format(dest_nick, args[1]))

    def rm_access(self, nick, args):
        if len(args) < 3:
            self.send("!auth forbid cmd nick")
            return
        if nick not in self.connected:
            self.send("You can't do that : connect before")
            return
        if args[1] not in self.access:
            return
        self.access[args[1]].remove(args[2])
        self.send("{0} can use {1} anymore ".format(args[2], args[1]))

    def show_access(self, nick, args):
        if len(args) < 2:
            self.send("!auth show cmd")
            return
        cmd = args[1]
        if cmd not in self.access or not len(self.access[cmd]):
            self.send("Nobody can access to that command")
            return
        self.send("Acces for command {0}: ".format(args[1]) +
            "|".join(self.access[args[1]]))

    def show_connected(self, nick, args):
        if not len(self.connected):
            self.send("Nobody is connected")
            return
        self.send("connected: " +
            "|".join(self.connected))
