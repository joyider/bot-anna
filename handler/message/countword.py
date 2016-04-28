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
from msghandler import PrivMsgHandler
from handler.command.command import CmdHandler


class CountMsgHandler(PrivMsgHandler):
    name = "countword"
    def __init__(self):
        super(CountMsgHandler, self).__init__()
        self.regexp = re.compile( self.Priv_Regexp +  "(?P<msg>.*)")
        self.dictionary = shelve.open("countword")

    def add_word(self, word):
        self.dictionary[word] = {}

    def notice_registration(self, bot):
        super(CountMsgHandler, self).notice_registration(bot)
        bot.register_cmd(ScoreCmd(self))
        bot.register_cmd(AddCountCmd(self))
        bot.register_cmd(ClearCountCmd(self))
        bot.register_cmd(ClearScoreCmd(self))
        self.loaded_commands = 4

    def handle(self, match):
        nick = match.group('nick')
        dest = match.group('dest')
        msg = match.group('msg').strip()

        if not dest.startswith("#"):
            return
        if msg.startswith("!"):
            return

        for word in self.dictionary.keys():
            word_dictionary = self.dictionary[word]
            count = msg.count(word)
            if count > 0:
                if nick not in word_dictionary:
                    word_dictionary[nick] = count
                else:
                    word_dictionary[nick] += count
                self.dictionary[word] = word_dictionary

    def notice_unregistration(self, quitting):
        self.loaded_commands -= 1
        if self.loaded_commands == 0:
            self.dictionary.close()

class ScoreCmd(CmdHandler):
    """Say to the bot to display the score of a followed word: !score <word>.\
 Without argument, shows the list of clearable words."""
    name = "score"
    access = {name : set(["all"])}

    def __init__(self, counter):
        super(ScoreCmd, self).__init__()
        self.regexp = re.compile(r"score$")
        self.counter = counter

    def handle(self, nick, dest, cmd, arg):
        arg = arg.strip()
        if not arg:
            self.send("The following words can be cleared: " +
                ", ".join(self.counter.dictionary.keys()))
            return
        if arg not in self.counter.dictionary:
            self.send("Unknow word {0}".format(arg))
            return

        score = self.counter.dictionary[arg]
        res = []
        podium = sorted(score, lambda x,y : cmp(score[x], score[y]), reverse=True)

        for i in range(min(3, len(podium))):
            res.append("{0}) with {1} point => {2}".format(
                i + 1, score[podium[i]], podium[i]))
        self.send("|".join(res))
        if not res:
          self.send("No score for word <{0}>.".format(arg))

    def notice_unregistration(self, quitting):
        self.counter.notice_unregistration(quitting)

class AddCountCmd(CmdHandler):
    """Say to the bot to follow a word: !addword <word>."""
    name = "addword"
    access = {name : set(["admin"])}

    def __init__(self, counter):
        super(AddCountCmd, self).__init__()
        self.regexp = re.compile(r"addword$")
        self.counter = counter

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if not args:
            self.send("This command needs and argument.")
            return
        word = args[0]
        if word in self.counter.dictionary:
            self.send("Word <{0}> already counted".format(word))
            return
        self.counter.add_word(word)
        self.send("Word <{0}> add to counter !".format(word))

    def notice_unregistration(self, quitting):
        self.counter.notice_unregistration(quitting)

class ClearCountCmd(CmdHandler):
    """Say to the bot to clear a word from the counter: !clearword <word>."""
    name = "clearword"
    access = {name : set(["admin"])}

    def __init__(self, counter):
        super(ClearCountCmd, self).__init__()
        self.regexp = re.compile(r"clearword$")
        self.counter = counter

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if not args:
            self.send("This command needs and argument.")
        elif args[0] in self.counter.dictionary:
            del self.counter.dictionary[args[0]]
            self.send("Word <{0}> cleared from the counter!".format(args[0]))
        else:
            self.send("Word <{0}> isn't in the counter!".format(args[0]))

    def notice_unregistration(self, quitting):
        self.counter.notice_unregistration(quitting)

class ClearScoreCmd(CmdHandler):
    """Say to the bot to clear the score of a word: !clearscore <word>."""
    name = "clearscore"
    access = {name : set(["admin"])}

    def __init__(self, counter):
        super(ClearScoreCmd, self).__init__()
        self.regexp = re.compile(r"clearscore$")
        self.counter = counter

    def handle(self, nick, dest, cmd, arg):
        args = arg.split()
        if not args:
            self.send("This command needs and argument.")
            return
        if args[0] not in self.counter.dictionary:
            self.send("Word <{0}> isn't in the counter!".format(args[0]))
            return
        self.counter.dictionary[args[0]] = {}
        self.send("The score of word <{0}> has been cleared!".format(args[0]))

    def notice_unregistration(self, quitting):
        self.counter.notice_unregistration(quitting)

