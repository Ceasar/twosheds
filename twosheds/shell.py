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

from .builtins import cd, export
from .cli import CommandLineInterface
from .completer import make_completer
from .request import Request
from .transform import (transform, AliasTransform, TildeTransform,
                        VariableTransform)

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
    # Marks the boundary between sentences
    SEP = ";"

    commands = {
        'cd': cd,
        'export': export,
    }

    def __init__(self,
                 environ,
                 aliases=None,
                 echo=False,
                 histfile=None,
                 use_suffix=True,
                 exclude=None,
                 ):
        super(Shell, self).__init__(environ)
        self.transforms = [
            AliasTransform(aliases),
            VariableTransform(os.environ),
            TildeTransform(os.environ['HOME']),
        ]
        self.completer = make_completer(
            transforms=self.transforms,
            use_suffix=use_suffix,
            exclude=exclude
        )
        self.echo = echo
        self.histfile = histfile or DEFAULT_HISTFILE

    def _save_history(self):
        readline.write_history_file(self.histfile)

    def eval(self, text):
        """Interpret the user's requests and respond to them.

        :param text: the user's input
        """
        for request in self.interpret(text):
            try:
                self.commands[request.command](*request.args)
            except KeyError:
                super(Shell, self).eval(request.text)

    def interpret(self, text):
        """Interpret the user's requests.

        :param text: the user's input
        """
        sentences = text.split(self.SEP)
        for sentence in sentences:
            if sentence:
                kernel_sentence = transform(sentence, self.transforms)
                if self.echo:
                    print kernel_sentence
                yield Request(kernel_sentence)

    def interact(self, banner=None):
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
        super(Shell, self).interact(banner)

    def add_command(self, command, func):
        self.commands[command] = func

    def command(self, command):
        def decoractor(f):
            self.add_command(command, f)
            return f
        return decoractor
