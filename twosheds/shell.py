"""

    twosheds.shell
    ~~~~~~~~~~~~~~

    This module implements the central user interface for access to an
    operating system's kernel services.

"""
import atexit
import os
import readline

from cli import CommandLineInterface

DEFAULT_HISTFILE = os.path.expanduser("~/.console-history")


class Shell(CommandLineInterface):
    """The shell is an sh-compatible command language interpreter that executes
    commands read from standard input.
    """
    def __init__(self, interpreter, histfile=DEFAULT_HISTFILE, prompt="$ "):
        self.interpreter = interpreter
        self.histfile = histfile
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
