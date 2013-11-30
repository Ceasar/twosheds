"""

    twosheds.shell
    ~~~~~~~~~~~~~~

    This module implements the central user interface for access to an
    operating system's kernel services.

"""
import sys
import traceback


class Shell(object):
    """The shell is an sh-compatible command language interpreter that executes
    commands read from standard input.
    """
    def __init__(self, interpreter):
        self.interpreter = interpreter

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
            return raw_input(self.prompt)
        except EOFError:
            raise SystemExit()

    def eval(self, line):
        """Evaluate a command."""
        self.interpreter.run(line)

    def interact(self, banner=None):
        """Interact with the user.
        
        The optional banner argument specifies the banner to print before the
        first interaction. By default, no banner is printed.
        """
        if banner:
            print(banner)
        while True:
            try:
                self.eval(self.read())
            except SystemExit:
                break
            except:
                self.error(traceback.format_exc())
