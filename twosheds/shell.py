"""

    twosheds.shell
    ~~~~~~~~~~~~~~

    This module implements the central user interface for access to an
    operating system's kernel services.

"""
import os
import subprocess
import sys
import traceback


class Shell(object):
    """The shell is an sh-compatible command language interpreter that executes
    commands read from standard input.
    """
    BUILTINS = {'cd': os.chdir}

    def __init__(self, aliases=None, builtins=None):
        self.aliases = aliases or {}
        self.builtins = builtins or self.BUILTINS

    @property
    def prompt(self):
        """Indicate to the user that the shell is waiting for a command."""
        return "$ "

    def output(self, msg):
        """Output a message."""
        sys.stdout.write(msg)

    def error(self, msg):
        """Output an error."""
        sys.stderr.write(msg)

    def read(self):
        """Accept a command from the user."""
        try:
            return self.expand(raw_input(self.prompt))
        except EOFError:
            raise SystemExit()

    def expand(self, line):
        """Expand any macros in a command."""
        new_tokens = []
        for token in line.split():
            try:
                v = self.aliases[token]
            except KeyError:
                if token.startswith("$"):
                    try:
                        v = os.environ[token[1:]]
                    except KeyError:
                        new_tokens.append(token)
                    else:
                        new_tokens.append(v)
                else:
                    new_tokens.append(token)
            else:
                new_tokens.append(v)
        return " ".join(new_tokens)

    def eval(self, line):
        """Evaluate an input."""
        tokens = line.split()
        command, args = tokens[0], tokens[1:]
        try:
            self.builtins[command](*args)
        except KeyError:
            subprocess.call(line, shell=True)

    def interact(self, banner=None):
        """Interact with the user.
        
        The optional banner argument specifies the banner to print before the
        first interaction. By default, no banner is printed.
        """
        if banner:
            print(banner)
        while True:
            try:
                line = self.read()
                if not line:
                    continue
                self.eval(line)
            except SystemExit:
                break
            except:
                self.error(traceback.format_exc())
