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
import math
from msghandler import PrivMsgHandler
from handler.command.command import CmdHandler

class SemanticMsgHandler(PrivMsgHandler):
    name = "semantic"
    active = False
    def __init__(self):
        super(SemanticMsgHandler, self).__init__()
        self.regexp = re.compile( self.Priv_Regexp +  "(?P<msg>.*)")
        self.personal_dict = shelve.open("semantic")

    def notice_registration(self, bot):
        super(SemanticMsgHandler, self).notice_registration(bot)
        bot.register_cmd(SemanticCmd(self))
        bot.register_cmd(PertinenceCmd(self))

    def match(self, msg):
        if not self.active:
            return None
        return self.regexp.match(msg)

    def handle(self, match):
        nick = match.group('nick')
        dest = match.group('dest')
        msg = match.group('msg').strip()

        if not dest.startswith("#"):
            return
        if msg.startswith("!"):
            return

        msg = msg.split()
        if nick not in self.personal_dict:
            self.personal_dict[nick] = {}
        dictionary = self.personal_dict[nick]
        for word in msg:
            word = word.strip('.;:,')
            if word not in dictionary:
                dictionary[word] = 1
            else:
                dictionary[word] += 1
        self.personal_dict[nick] = dictionary

    def notice_unregistration(self, quitting):
        self.personal_dict.close()

class SemanticCmd(CmdHandler):
    """Control the state of the semantic module: !semantic <start|stop>."""
    name = "semantic"
    noregister = True

    def __init__(self, module):
        super(SemanticCmd, self).__init__()
        self.regexp = re.compile(r"semantic$")
        self.module = module

    def handle(self, nick, dest, cmd, arg):
        arg = arg.strip()
        if not arg:
            self.send("This command needs an argument!")
        if arg != "start" and arg != "stop":
            self.send("Unknown command <{0}>!".format(arg))
            return

        active = arg == "start"
        if active == self.module.active:
            self.send("Module semantic is already in asked state!")
        self.module.active = active

    def notice_unregistration(self, quitting):
        self.module.self_unload()

class PertinenceCmd(CmdHandler):
    """Return the global tf-idf of a person: !pertinence <nick>."""
    name = "pertinence"
    noregister = True

    def __init__(self, counter):
        super(PertinenceCmd, self).__init__()
        self.regexp = re.compile(r"pertinence$")
        self.counter = counter

    def handle(self, nick, dest, cmd, arg):
        arg = arg.strip()
        if arg not in self.counter.personal_dict:
            self.send("Nickname <{0}> unknown!".format(arg))
            return

        tfidf = 0.0
        corpus_size = float(len(self.counter.personal_dict))
        max_frequency = float(max(self.counter.personal_dict[arg].values()))
        for word in self.counter.personal_dict[arg].keys():
            corpus_appearance = reduce(lambda x,y: x + 1 if word in y else x,
                                       self.counter.personal_dict.values(), 0)
            document_frequency = self.counter.personal_dict[arg][word]
            tfidf += document_frequency/max_frequency * math.log(corpus_size/corpus_appearance)

        self.send("Global pertinence of {0} is {1}!".format(arg, tfidf))

    def notice_unregistration(self, quitting):
        pass
