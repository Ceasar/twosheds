"""
twosheds.shell
~~~~~~~~~~~~~~

This module implements the central user interface for access to an
operating system's kernel services.
"""
from __future__ import absolute_import

import atexit
import os
try:
    import readline
except ImportError:
    import pyreadline as readline

from .cli import CommandLineInterface
from .completer import make_completer
from .terminal import Terminal

DEFAULT_HISTFILE = os.path.expanduser("~/.console-history")


class Shell(CommandLineInterface):
    """
    A facade encapsulating the high-level logic of a command language
    interpreter.

    :param aliases: dictionary of aliases
    :param builtins: dictionary of builtins
    :param echo: set True to print commands immediately before execution
    :param environ:
        a dictionary containing environmental variables. This must include PS1
        and PS2, which are used to define the prompts.
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
        >>> shell.interact()  # doctest: +SKIP
    """

    def __init__(self,
                 environ,
                 aliases=None,
                 echo=False,
                 histfile=None,
                 use_suffix=True,
                 exclude=None,
                 ):
        super(Shell, self).__init__(aliases, Terminal(environ))
        self.completer = make_completer(
            transforms=self.transforms,
            use_suffix=use_suffix,
            exclude=exclude
        )
        self.echo = echo
        self.histfile = histfile or DEFAULT_HISTFILE
        self._before_interaction_funcs = []
        self._after_interaction_funcs = []

    def _save_history(self):
        readline.write_history_file(self.histfile)

    def serve_forever(self, banner=None):
        """Interact with the user.

        :param banner: (optional) the banner to print before the first
                       interaction. Defaults to ``None``.
        """
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(self.histfile)
            except IOError:
                pass
            atexit.register(self._save_history)
        super(Shell, self).serve_forever(banner)

    def interact(self):
        for f in self._before_interaction_funcs:
            f()
        super(Shell, self).interact()
        for f in self._after_interaction_funcs:
            f()

    def add_command(self, command, func):
        self.commands[command] = func

    def command(self, command):
        def decoractor(f):
            self.add_command(command, f)
            return f
        return decoractor

    def before_interaction(self, f):
        """Register a function to be run before each interaction.

        :param f:
            The function to run after each interaction. This function must not
            take any parameters.

        """
        self._before_interaction_funcs.append(f)
        return f

    def after_interaction(self, f):
        """Register a function to be run after each interaction.

        :param f:
            The function to run after each interaction. This function must not
            take any parameters.

        """
        self._after_interaction_funcs.append(f)
        return f
