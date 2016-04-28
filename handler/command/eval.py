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


class EvalCmdHandler(CmdHandler):
    """Eval python commands : !eval <python code>"""
    name = "eval"
    access = {name : set(['admin'])}

    allowed_func = ["dir",
        "dict", "type", "set", "list", "range", "pow", "ord", "hex",
        "oct", "bin", "int", "all", "any", "bool", "hash", "map", "reduce"
        ]

    def __init__(self):
        super(EvalCmdHandler, self).__init__()
        self.regexp = re.compile(r"eval$")
        self.locals = {}
        for f in EvalCmdHandler.allowed_func:
            self.locals.update({f : eval(f)})

    def handle(self, nick, dest, cmd, arg):
        if (arg.count("import") or arg.count("__subclasses__") or
                arg.count("__bases__") or arg.count("__builtins__")):
            self.send("I can't sorry..")
            return
        try :
            res = eval(arg.strip() , {"__builtins__":None}, self.locals)
            self.send(res)
        except SyntaxError as e:
            self.send("Syntax Error !")

        except Exception as e:
            self.send(str(e))
        except SystemExit as e:
            self.send("I don't wanna die ='(")
