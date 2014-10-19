"""

twosheds.program
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the Program object which represents Bash programs.
"""
from .kernel import Kernel
from .sentence import Sentence
from .transform import transform
import token


QUOTES = ("'", '"')


class Program(object):
    """
    This represents a sequence of procedures expressed in a programming
    language.

    >>> program = Program("ls -a")
    >>> list(program.gen_tokens())
    ['ls', '-a']
    """
    def __init__(self, text, transforms=None, echo=False):
        self.text = text

        # Token recognition variables
        self.blanks = {' ', '\t'}
        self.escape_chars = {'\\'}
        self.metacharacters = {"|", "&", ";", "(", ")"} | self.blanks
        self.whitespace = self.blanks | {'\r', '\n'}

        self.transforms = transforms or []

        self.echo = echo

    def gen_tokens(self):
        """
        >>> list(Program("ls").gen_tokens())
        ['ls']
        >>> list(Program("ls -a").gen_tokens())
        ['ls', '-a']
        >>> list(Program("cd /; pwd").gen_tokens())
        ['cd', '/', None, 'pwd']
        >>> list(Program("'cd /; pwd'").gen_tokens())
        ['cd /; pwd']
        """
        current_token = []
        escape = False
        quote = None
        skip = 0
        for char, peek in zip(self.text, self.text[1:] + " "):
            if skip > 0:
                skip -= 1
                continue
            if quote is None:
                if escape:
                    current_token.append(char)
                    escape = False
                elif char in self.escape_chars:
                    escape = True
                elif char in QUOTES:
                    quote = char
                elif char in self.metacharacters:
                    if current_token:
                        yield token.Word(''.join(current_token))
                    current_token = []
                    if char == "(":
                        yield token.LParen()
                    elif char == ")":
                        yield token.RParen()
                    elif char in "|&;":
                        if peek == char:
                            yield token.Word(char + peek)
                            skip += 1
                        else:
                            yield token.Word(char)
                else:
                    current_token.append(char)
            elif char == quote:
                if current_token:
                    yield token.DoubleQuote(''.join(current_token))
                current_token = []
                quote = None
            else:
                current_token.append(char)
        if quote is not None:
            raise ValueError("No closing quotation")
        if escape:
            raise ValueError("No escaped character")
        if current_token:
            yield token.Word(''.join(current_token))

    def _gen_sentences(self, tokens):
        sentence = []
        for token in tokens:  # noqa
            if str(token) == ";":
                yield sentence
                sentence = []
            else:
                sentence.append(token)
        yield sentence

    def gen_sentences(self, tokens, aliases=None):
        """
        Generate a sequence of sentences from stream of tokens.
        """
        if aliases is None:
            aliases = {}
        for sentence in self._gen_sentences(tokens):
            try:
                alias = aliases[str(sentence[0])]
            except KeyError:
                # do nothing if no alias is found
                pass
            except IndexError:
                pass
            else:
                sentence[0:1] = list(Program(alias).gen_tokens())
            yield transform(Sentence(sentence), self.transforms)

    def interpret(self, sentence, environ=None):
        if environ is None:
            environ = {}
        try:
            return environ[sentence.command](*sentence.args)
        except KeyError:
            return Kernel().respond(str(sentence))
        except IndexError:
            return None

    def run(self, aliases=None, environ=None):
        tokens = self.gen_tokens()
        for sentence in self.gen_sentences(tokens, aliases):
            self.interpret(sentence, environ)
