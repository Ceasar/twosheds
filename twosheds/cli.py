import sys
import traceback


DEFAULT_PROMPT = "$ "

class CommandLineInterface(object):
    """
    Basic read-eval-print loop.
    """
    def __init__(self, prompt=DEFAULT_PROMPT):
        self._prompt = prompt

    @property
    def prompt(self):
        """Indicate to the user that the shell is waiting for a command."""
        return self._prompt

    def read(self):
        """Accept a command from the user."""
        try:
            return raw_input(self.prompt)
        except EOFError:
            raise SystemExit()

    def eval(self, line):
        """Evaluate a command."""
        raise NotImplementedError()

    def output(self, msg):
        """Output a message."""
        sys.stdout.write(msg)

    def error(self, msg):
        """Output an error."""
        sys.stderr.write(msg)

    def interact(self, banner=None):
        """Interact with the user.
        
        The optional banner argument specifies the banner to print before the
        first interaction. By default, no banner is printed.
        """
        if banner:
            print(banner)
        while True:
            try:
                rv = self.eval(self.read())
                if rv is not None:
                    self.output(rv)
            except SystemExit:
                break
            except:
                self.error(traceback.format_exc())
