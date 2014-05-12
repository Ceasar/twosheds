import sys
import traceback

from .kernel import Kernel


class CommandLineInterface(object):
    """
    Basic read-eval-print loop.

    :param environ:
        a dictionary containing environmental variables

    """
    # Marks the boundary between sentences
    SEP = ";"

    def __init__(self, environ):
        self.environ = environ
        self._kernel = Kernel()

    @property
    def primary_prompt_string(self):
        """The prompt first seen at the command line. Defaults to "$ "."""
        return self.environ.get("PS1", "$ ")

    @property
    def secondary_prompt_string(self):
        """The prompt seen for line continuations. Defaults to "> "."""
        return self.environ.get("PS2", "> ")

    def read(self):
        """Prompt the user and read a command from the terminal.

        A backslash followed by a <newline> is interpreted as a line
        continuation. The backslash and <newline>s are removed before splitting
        the input into tokens.

        For example:

            $ uname \
            > -m
            x86_64

        Returns a strings containing the user's input.
        """
        try:
            line = raw_input(self.primary_prompt_string)
            while line.endswith("\\"):
                line = line[:-1] + raw_input(self.secondary_prompt_string)
        except EOFError:
            raise SystemExit()
        else:
            return line

    def interpret(self, text):
        """Interpret the user's input.

        :param text: the user's input
        """
        return text.split(self.SEP)

    def respond(self, sentence):
        """Respond to command from the user. Optionally returns a string to
        print to standard out.

        :param sentence: the user's command
        """
        return self._kernel.respond(sentence)

    def eval(self, text):
        """Respond to text entered by the user.

        :param text: the user's input
        """
        for sentence in self.interpret(text):
            if sentence:
                try:
                    response = self.respond(sentence)
                except SystemExit:
                    break
                except:
                    self.error(traceback.format_exc())
                else:
                    if response is not None:
                        self.output(response)

    def interact(self):
        """Get a command from the user and respond to it."""
        self.eval(self.read())

    def serve_forever(self, banner=None):
        """Handle one interaction at a time until shutdown.

        :param banner: (optional) the banner to print before the first
                       interaction. Defaults to ``None``.
        """
        if banner:
            print(banner)
        while True:
            self.interact()

    def output(self, msg):
        """Output a message.

        :param msg: a string to print to standard out
        """
        sys.stdout.write(msg)

    def error(self, msg):
        """Output an error.

        :param msg: a string to print to standard error
        """
        sys.stderr.write(msg)
