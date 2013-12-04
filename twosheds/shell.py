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
from .grammar import Grammar
from .language import Language
from .semantics import Semantics
from .transformation import AliasTransformation, TildeTransformation, VariableTransformation

DEFAULT_HISTFILE = os.path.expanduser("~/.console-history")


class Shell(CommandLineInterface):
    """
    A facade encapsulating the high-level logic of a command language
    interpreter.

    :param aliases: dictionary of aliases
    :param builtins: dictionary of builtins
    :param echo: set True to print commands immediately before execution
    :param prompt: the string which is printed before reading each command
                   from the terminal.
    :param histfile: the location in which to look for a history file. if
                     unset, ``DEFAULT_HISTFILE`` is used. histfile is useful
                     when sharing the same home directory between different
                     machines, or when saving separate histories on different
                     terminals.
    :param use_suffix: add a ``/`` to completed directories and a space to the
                       end of other completed words, to speed typing and
                       provide a visual indicator of successful completion.
    :param exclude: list of regexes to be ignored by completion.

    Usage::

        >>> import twosheds
        >>> shell = twosheds.Shell()
        >>> shell.interact()
    """
    def __init__(self,
                 aliases=None,
                 builtins=None,
                 echo=False,
                 prompt=None,
                 histfile=None,
                 use_suffix=True,
                 exclude=None,
                 ):
        super(Shell, self).__init__(prompt)

        transformations = [AliasTransformation(aliases),
                           TildeTransformation(),
                           VariableTransformation(os.environ),
                           ]
        grammar = Grammar(echo=echo, transformations=transformations)
        semantics = Semantics(builtins)
        self.language = Language(grammar, semantics)

        self.completer = Completer(grammar, use_suffix=use_suffix, exclude=exclude)
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

    def eval(self, text):
        """Interpret and respond to user input. Optionally returns a string to
        print to standard out.
        
        :param text: the user's input
        """
        return self.language.interpret(text)
