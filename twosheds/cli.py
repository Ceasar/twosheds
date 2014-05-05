import sys
import traceback


DEFAULT_PROMPT = "$ "


class CommandLineInterface(object):
    """
    Basic read-eval-print loop.

    :param prompt: (optional) the string which is printed before reading each
                   command from the terminal. Defaults to "$ ".
    """
    def __init__(self, prompt=None):
        self._prompt = prompt or DEFAULT_PROMPT

    @property
    def prompt(self):
        """
        The string which is printed before reading each command from the
        terminal.
        """
        return self._prompt

    def read(self):
        """Prompt the user and read the user input.

        A backslash followed by a <newline> is interpreted as a line
        continuation. The backslash and <newline>s are removed before splitting
        the input into tokens.

        For example:

            $ uname \
            > -m
            x86_64

        Returns a string containing the user's input.
        """
        try:
            line = raw_input(self.prompt)
            while line.endswith("\\"):
                line = line[:-1] + raw_input("> ")
            return line
        except EOFError:
            raise SystemExit()

    def eval(self, text):
        """Interpret and respond to user input. Optionally returns a string to
        print to standard out.

        :param text: the user's input
        """
        raise NotImplementedError()

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
            try:
                response = self.eval(self.read())
                if response is not None:
                    self.output(response)
            except SystemExit:
                break
            except:
                self.error(traceback.format_exc())
