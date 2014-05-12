import os
import traceback

from program import Program
from builtins import cd, export
from .transform import TildeTransform, VariableTransform


class CommandLineInterface(object):
    """
    Basic read-eval-print loop.
    """
    commands = {
        'cd': cd,
        'export': export,
    }

    def __init__(self, aliases, terminal, echo=False):
        self.aliases = aliases
        self.terminal = terminal
        self.echo = echo
        self.transforms = [
            VariableTransform(os.environ),
            TildeTransform(os.environ['HOME']),
        ]

    def read(self):
        """
        The shell shall read its input in terms of lines from a file, from a
        terminal in the case of an interactive shell, or from a string in the
        case of sh -c or system(). The input lines can be of unlimited length.
        """
        for line in self.terminal:
            yield line

    def eval(self, text):
        """Respond to text entered by the user.

        :param text: the user's input
        """
        program = Program(text, echo=self.echo, transforms=self.transforms)
        tokens = program.gen_tokens()
        for sentence in program.gen_sentences(tokens, self.aliases):
            if self.echo:
                self.terminal.debug(str(sentence))
            program.interpret(sentence, self.commands)

    def interact(self):
        """Get a command from the user and respond to it."""
        lines = ""
        for line in self.read():
            lines += line
            try:
                self.eval(lines)
            except ValueError:
                pass
            except:
                self.terminal.error(traceback.format_exc())
                break
            else:
                break

    def serve_forever(self, banner=None):
        """Handle one interaction at a time until shutdown.

        :param banner: (optional) the banner to print before the first
                       interaction. Defaults to ``None``.
        """
        if banner:
            print(banner)
        while True:
            self.interact()
