"""

    twosheds.shell
    ~~~~~~~~~~~~~~

    This module implements the central user interface for access to an
    operating system's kernel services.

"""
import atexit
import code
import os
import readline
from subprocess import call, check_output
import sys
import traceback


class Shell(object):
    """The shell is an sh-compatible command language interpreter that executes
    commands read from standard input.
    """
    BUILTINS = {'cd': os.chdir}

    def __init__(self, aliases=None, builtins=None,
                 histfile=os.path.expanduser("~/.console-history")):
        self.aliases = aliases or {}
        self.builtins = builtins or self.BUILTINS
        self.init_history(histfile)

    @property
    def prompt(self):
        """Indicate to the user that the shell is waiting for a command."""
        return "$"

    def output(self, msg):
        """Output a message."""
        sys.stdout.write(msg)

    def error(self, msg):
        """Output an error."""
        sys.stderr.write(msg)

    def read(self):
        """Accept a command from the user."""
        try:
            return self.rewrite(raw_input(self.prompt))
        except EOFError:
            raise SystemExit()

    def rewrite(self, line):
        """Transform a line."""
        tokens = line.split()
        new_tokens = []
        for token in tokens:
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

    def _raise_cursor(self, n=1):
        """Move the cursor up `n` lines."""
        self.output('\033[%sA' % n)
        sys.stdout.flush()

    def _clear_line(self):
        self.output('\033[K')
        sys.stdout.flush()

    def eval(self, line):
        """Evaluate an input."""
        call(line, shell=True)

    def interact(self):
        """"""
        while True:
            try:
                line = self.read()
                if not line:
                    continue
                tokens = line.split()
                command, args = tokens[0], tokens[1:]
                # handle any shell builtin commands
                try:
                    self.builtins[command](*args)
                except KeyError:
                    self.eval(line)
                self.after(line)
            except SystemExit:
                break
            except:
                self.error(traceback.format_exc())

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.
        
        The completion should begin with 'text'.
        """
        matches = []

        head, tail = os.path.split(text)

        ls = check_output("ls %s" % head, shell=True)
        filenames = ls.split()

        for filename in filenames:
            if filename.startswith(tail):
                matches.append(os.path.join(head, filename))
        try:
            return matches[state]
        except IndexError:
            return None

    def init_history(self, histfile):
        if sys.platform == 'darwin':
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)
