import sys


class Terminal(object):
    """An interface for text entry and display."""
    def __init__(self, environ):
        self.environ = environ

    @property
    def primary_prompt_string(self):
        """The prompt first seen at the command line. Defaults to "$ "."""
        return self.environ.get("PS1", "$ ")

    @property
    def secondary_prompt_string(self):
        """The prompt seen for line continuations. Defaults to "> "."""
        return self.environ.get("PS2", "> ")

    @property
    def quaternary_prompt_string(self):
        """Printed before each command displayed during an execution trace"""
        return self.environ.get("PS4", "+ ")

    def readline(self, continuation=False):
        """Read a line from the terminal.

        A backslash followed by a <newline> is interpreted as a line
        continuation. The backslash and <newline>s are removed before return.

        For example::

            $ uname \
            > -m
            x86_64

        :param continuation:
            True if the line is a continuation. Defaults to False.
        """
        prompt = (self.secondary_prompt_string if continuation else
                  self.primary_prompt_string)
        try:
            line = raw_input(prompt)
            while line.endswith("\\"):
                line = line[:-1] + raw_input(self.secondary_prompt_string)
        except EOFError:
            raise SystemExit()
        else:
            return line

    def readlines(self):
        """Read a command from the terminal.

        Returns a list of tokens containing the user's input.
        """
        continuation = False
        while True:
            yield self.readline(continuation)
            continuation = True

    def __iter__(self):
        return self.readlines()

    def write(self, msg):
        """Output a message.

        :param msg: a string to print to standard out
        """
        sys.stdout.write(msg)

    def debug(self, msg):
        print self.quaternary_prompt_string + msg

    def error(self, msg):
        """Output an error.

        :param msg: a string to print to standard error
        """
        sys.stderr.write(msg)
