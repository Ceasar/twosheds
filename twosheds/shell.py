"""

    twosheds.shell
    ~~~~~~~~~~~~~~

    This module implements the central user interface for access to an
    operating system's kernel services.

"""
from __future__ import absolute_import

import atexit
import os
import readline
import sys

from .cli import CommandLineInterface
from .completer import Completer
from .interpreter import Interpreter

DEFAULT_HISTFILE = os.path.expanduser("~/.console-history")


class Shell(CommandLineInterface):
    """The shell is an sh-compatible command language interpreter that executes
    commands read from standard input.

    Shell is a facade encapsulating the high-level logic of a twosheds system.
    """
    def __init__(self,
                 aliases=None,
                 builtins=None,
                 prompt=None,
                 histfile=None,
                 use_suffix=True,
                 exclude=None,
                 ):
        super(Shell, self).__init__(prompt)

        self.interpreter = Interpreter(aliases, builtins)

        self.completer = Completer(use_suffix=use_suffix, exclude=exclude)
        readline.parse_and_bind("bind ^I rl_complete" if sys.platform == 'darwin'
                                else "tab: complete")
        readline.set_completer(self.completer.complete)

        self.histfile = histfile or DEFAULT_HISTFILE,
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self._save_history)

    def _save_history(self):
        readline.write_history_file(self.histfile)

    def eval(self, line):
        return self.interpreter.run(line)
