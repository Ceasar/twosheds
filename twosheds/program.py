"""

twosheds.program
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the Program object which represents Bash programs.
"""
from .kernel import Kernel
from .sentence import Sentence
from .transform import transform


QUOTES = ("'", '"')
KERNEL = Kernel()


class Program(object):
    """
    This represents a sequence of procedures expressed in a programming
    language.

    >>> program = Program("ls -a")
    >>> list(program.gen_tokens())
    ['ls', '-a']
    """
    def __init__(self, tokens, transforms=None):
        self.tokens = tokens
        self.transforms = transforms or []

    def _gen_sentences(self, tokens):
        sentence = []
        for token in tokens:  # noqa
            if str(token) == ";":
                yield sentence
                sentence = []
            else:
                sentence.append(token)
        yield sentence

    def gen_sentences(self):
        """
        Generate a sequence of sentences from stream of tokens.
        """
        for sentence in self._gen_sentences(self.tokens):
            yield transform(Sentence(sentence), self.transforms)

    def interpret(self, sentence, environ=None):
        if environ is None:
            environ = {}
        try:
            return environ[sentence.command](*sentence.args)
        except KeyError:
            return KERNEL.respond(str(sentence))
        except IndexError:
            return None

    def run(self, aliases=None, environ=None):
        tokens = self.gen_tokens()
        for sentence in self.gen_sentences(tokens, aliases):
            self.interpret(sentence, environ)
