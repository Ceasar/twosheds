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
            lines = self.lex(raw_input(self.prompt)).split(";")
            for line in lines:
                yield self.expand(line)
        except EOFError:
            raise SystemExit()

    def lex(self, line):
        return line.replace(";", " ; ")

    def expand_aliases(self, line):
        """Expand aliases in a line."""
        try:
            command, args = line.split(" ", 1)
        except ValueError:
            command, args = line, ""
        try:
            return "%s %s" % (self.aliases[command], args)
        except KeyError:
            return line

    def expand_variables(self, line):
        """Expand environmental variables in a line."""
        tokens = line.split()
        new_tokens = []
        for token in tokens:
            if token.startswith("$"):
                try:
                    token = os.environ[token[1:]]
                except KeyError:
                    pass
            new_tokens.append(token)
        return " ".join(new_tokens)

    def expand(self, line):
        """Expand any macros in a command."""
        return self.expand_variables(self.expand_aliases(line))

    def eval(self, line):
        """Evaluate an input."""
        if not line:
            return
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
                for command in self.read():
                    self.eval(command)
            except SystemExit:
                break
            except:
                self.error(traceback.format_exc())
