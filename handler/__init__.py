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
# Timesamp: 4/28/16 :: 10:41 PM

import message
import command
from irchandler import IrcHandler
from message.msghandler import MsgHandler

def get(module, attr):
    return module.__getattribute__(attr)


def load_handlers():
    for mod_name in message.__all__:
        msg_handlers.update(load_submodule(message, mod_name, classfilter=MsgHandler))

    for mod_name in command.__all__:
        cmd_handlers.update(load_submodule(command, mod_name, classfilter=IrcHandler))

def load_submodule(surmod, mod_name, classfilter=None):
    res = {}
    module = get(surmod, mod_name)
    for h_name in dir(module):
        h = get(module, h_name)
        if type(h) == type(type) and classfilter and issubclass(h, classfilter):
            if hasattr(h, "name") and h.name:
                res.update({h.name : h})
    return res



def reload_command(mod_name):
    global command
    reload (command)
    if mod_name not in dir(command):
        return False

    reload(get(command, mod_name))
    cmd_handlers.update(load_submodule(command, mod_name, classfilter=IrcHandler))
    return True

def reload_message(mod_name):
    global message
    reload (message)
    if mod_name not in dir(message):
        return False

    reload(get(message, mod_name))
    msg_handlers.update(load_submodule(message, mod_name, classfilter=MsgHandler))
    return True


#On import
msg_handlers = {}
cmd_handlers = {}
load_handlers()

__all__ = ['cmd_handlers', 'msg_handlers', 'reload_command', 'reload_message']