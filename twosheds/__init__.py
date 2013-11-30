#-*- coding:utf-8 -*-

from __future__ import absolute_import

import readline
import sys

from .completer import Completer
from .history import History, DEFAULT_HISTFILE
from .interpreter import Interpreter
from .shell import Shell


def get_shell(aliases=None,
              builtins=None,
              exclude=None,
              histfile=DEFAULT_HISTFILE,
              use_suffix=True,
              ):
    history = History(histfile)
    completer = Completer(use_suffix=use_suffix, exclude=exclude)
    readline.parse_and_bind("bind ^I rl_complete" if sys.platform == 'darwin'
                            else "tab: complete")
    readline.set_completer(completer.complete)
    interpreter = Interpreter(aliases, builtins)
    return Shell(interpreter)
