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
import shelve
from os import mkdir, path, unlink

from command import CmdHandler



class EventException(Exception):
    pass

class Event(object):
    def __init__(self, name, descr=""):
        self.name = name
        self.descr = descr
        self.registered = []
        self.allowed_chans = []

    def register(self, chan, nick):
        if ('all' not in self.allowed_chans and
            chan not in self.allowed_chans):
            raise EventException("Registration from non allowed chan")
        if nick in self.registered:
            raise EventException("<{0}> already registered".format(nick))
        self.registered.append(nick)

    def unregister(self, chan, nick):
        if nick not in self.registered:
            raise EventException("<{0}> is not registered for this event".format(nick))
        self.registered.remove(nick)

    def allowchan(self, chan):
        self.allowed_chans.append(chan)

    def forbidchan(self, chan):
        self.allowed_chans.remove(chan)

    def __iter__(self):
        for reg in self.registered:
            yield reg

    def __len__(self):
        return len(self.registered)


class EventCmdHandler(CmdHandler):
    name = "events"
    access = {name : set(['admin'])}
    noregister = True

    def __init__(self, serv_addr, serv_dir):
        self.sons = []
        self.base_dir = serv_dir
        self.base_addr = serv_addr
        self.events = shelve.open("events")

        if not path.exists(self.base_dir + "/events/"):
            mkdir(self.base_dir + "/events/")

    def match(self, *args):
        return False

    def handle(self, *args):
        raise NotImplemented

    def get_event_page(self, eventname):
        return self.base_addr + "/events/" + eventname

    def get_event_path(self, eventname):
        return self.base_dir + "/events/" + eventname

    def refresh_page(self, eventname):
        if eventname not in self.events:
            unlink(self.get_event_path(eventname))
            return
        f = open(self.get_event_path(eventname), "w+")


        e = self.events[eventname]
        if not len(e):
            f.write("Nobody is  registered for event : {0}\n({1})\n\n".format(eventname, e.descr))
            return
        f.write("People registered for event : {0}\n({1})\n\n".format(eventname, e.descr))
        for nick in e:
            f.write("   * {0}\n".format(nick))
        f.close()

    def notice_registration(self, cmd_dispatcher):
        super(EventCmdHandler, self).notice_registration(cmd_dispatcher)

        self.sons.append(AddEventCmdHandler(self))
        self.sons.append(RmEventCmdHandler(self))
        self.sons.append(ListEventCmdHandler(self))
        self.sons.append(RegisterCmdHandler(self))
        self.sons.append(UnRegisterCmdHandler(self))
        for son in self.sons:
            cmd_dispatcher.register(son)

    def notice_unregistration(self, quitting):
        super(EventCmdHandler, self).notice_unregistration(quitting)
        for son in self.sons:
            son.self_unload()
        self.events.close()

class AddEventCmdHandler(CmdHandler):
    """add event"""
    name = "addevent"
    access ={name : set(['admin'])}
    noregister = True

    def __init__(self, dad):
        super(AddEventCmdHandler, self).__init__()
        self.regexp = re.compile(self.name + "$")
        self.dad = dad

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if len(args) < 1:
            self.send("!{0} eventname [descr]".format(self.name))
            return
        eventname = args[0]
        descr = ""
        if len(args) > 1:
            descr = " ".join(args[1:])
        if eventname in self.dad.events:
            self.send("event <{0}> already exist !".format(eventname))
            return

        e = Event(eventname, descr)
        e.allowchan(dest)
        self.dad.events[eventname] = e

        self.dad.refresh_page(eventname)
        self.send("Event <{0}> created: list is at addr \"{1}\"".format(
                    eventname, self.dad.get_event_page(eventname)))

class RmEventCmdHandler(CmdHandler):
    """rm event"""
    name = "rmevent"
    access ={name : set(['admin'])}
    noregister = True

    def __init__(self, dad):
        super(RmEventCmdHandler, self).__init__()
        self.regexp = re.compile(self.name + "$")
        self.dad = dad

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if len(args) < 1:
            self.send("!{0} eventname".format(self.name))
            return
        eventname = args[0]
        if eventname not in self.dad.events:
            self.send("event <{0}> doesn't exist !".format(eventname))
            return
        del self.dad.events[eventname]
        self.dad.refresh_page(eventname)
        self.send("Event <{0}> removed".format(eventname))

class ListEventCmdHandler(CmdHandler):
    """list event"""
    name = "listevent"
    access ={name : set(['all'])}
    noregister = True

    def __init__(self, dad):
        super(ListEventCmdHandler, self).__init__()
        self.regexp = re.compile(self.name + "$")
        self.dad = dad

    def handle(self, nick, dest, cmd, arg):
        if not len(self.dad.events):
            self.send("No events, sorry :(")
            return
        self.send("| ".join(self.dad.events))

class RegisterCmdHandler(CmdHandler):
    """register event"""
    name = "register"
    access ={name : set(['all'])}
    noregister = True

    def __init__(self, dad):
        super(RegisterCmdHandler, self).__init__()
        self.regexp = re.compile(self.name + "$")
        self.dad = dad

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if len(args) < 1:
            self.send("!{0} eventname".format(self.name))
            return
        eventname = args[0]
        if not eventname in self.dad.events:
            self.send("Unknow event sorry")
            return
        #Tricks for shelve with no traceback
        e = self.dad.events[eventname]
        try:
            e.register(dest, nick)
        except EventException as e:
            self.send(e)
            return
        self.dad.events[eventname] = e
        self.dad.refresh_page(eventname)
        self.send("You are now registered for event <{0}>".format(eventname))


class UnRegisterCmdHandler(CmdHandler):
    """unregister event"""
    name = "unregister"
    access ={name : set(['all'])}
    noregister = True

    def __init__(self, dad):
        super(UnRegisterCmdHandler, self).__init__()
        self.regexp = re.compile(self.name + "$")
        self.dad = dad

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if len(args) < 1:
            self.send("!{0} eventname".format(self.name))
            return
        eventname = args[0]
        if not eventname in self.dad.events:
            self.send("Unknow event sorry")
            return

        e = self.dad.events[eventname]
        try:
            e.unregister(dest, nick)
        except EventException as e:
            self.send(e)
            return
        self.dad.events[eventname] = e
        self.dad.refresh_page(eventname)
        self.send("You are no longer registered for event <{0}>".format(eventname))
