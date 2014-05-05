import sys
import traceback

from .kernel import Kernel


class CommandLineInterface(object):
    """
    Basic read-eval-print loop.

    :param environ:
        a dictionary containing environmental variables

    """
    def __init__(self, environ):
        self.environ = environ
        self._kernel = Kernel()
        self._before_request_funcs = []
        self._after_request_funcs = []

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

        Returns a string containing the user's command.
        """
        try:
            line = raw_input(self.primary_prompt_string)
            while line.endswith("\\"):
                line = line[:-1] + raw_input(self.secondary_prompt_string)
            return line
        except EOFError:
            raise SystemExit()

    def eval(self, text):
        """Interpret and respond to user input. Optionally returns a string to
        print to standard out.

        :param text: the user's input
        """
        return self._kernel.respond(text)

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

    def interact(self, banner=None):
        """Interact with the user.

        :param banner: (optional) the banner to print before the first
                       interaction. Defaults to ``None``.
        """
        if banner:
            print(banner)
        while True:
            for f in self._before_request_funcs:
                f()
            try:
                response = self.eval(self.read())
                if response is not None:
                    self.output(response)
            except SystemExit:
                break
            except:
                self.error(traceback.format_exc())
            for f in self._after_request_funcs:
                f()

    def before_request(self, f):
        """Register a function to be run before each interaction.

        :param f:
            The function to run after each request. This function must not take
            any parameters.

        """
        self._before_request_funcs.append(f)
        return f

    def after_request(self, f):
        """Register a function to be run after each interaction.

        :param f:
            The function to run after each request. This function must not take
            any parameters.

        """
        self._after_request_funcs.append(f)
        return f
