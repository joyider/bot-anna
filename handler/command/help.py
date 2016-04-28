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

class HelpCmdHandler(CmdHandler):
  """Help command. Give help on the loaded command of the bot."""

  name = "help"
  access = {"help" : set(["all"])}

  def __init__(self):
      super(HelpCmdHandler, self).__init__()
      self.regexp = re.compile(r"help$")

  def notice_registration(self, cmd_dispatcher):
      self.cmd_handlers = cmd_dispatcher.handlers;

  def handle(self, nick, dest, cmd, arg):
      args = arg.split()
      if (len(args) == 1) and args[0] in self.cmd_handlers:
          cmdhandler = self.cmd_handlers[args[0]];
          if (cmdhandler.__doc__ is not None):
              self.send(cmdhandler.__doc__)
              return
      msg = "Commands are accessible with !CMD. You can also get more help "
      msg += "with !help CMD. The list of available commands is: "
      msg += ", ".join([c.name for c in self.cmd_handlers.values() if c.__doc__
                        is not None])
      msg += "."
      self.send(msg)
