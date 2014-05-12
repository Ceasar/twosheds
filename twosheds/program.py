from .kernel import Kernel
from .sentence import Sentence
from .transform import transform


class Program(object):
    def __init__(self, text, transforms=None, echo=False):
        self.text = text

        # Token recognition variables
        self.escape_chars = {'\\'}
        self.quotes = {"'", '"'}
        self.separators = ";"
        self.whitespace = {' ', '\t', '\r', '\n'}

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
        for char in self.text:
            if quote is None:
                if escape:
                    current_token.append(char)
                    escape = False
                elif char in self.escape_chars:
                    escape = True
                elif char in self.quotes:
                    quote = char
                elif char in self.whitespace:
                    if current_token:
                        yield ''.join(current_token)
                    current_token = []
                elif char in self.separators:
                    if current_token:
                        yield ''.join(current_token)
                    current_token = []
                    yield None
                else:
                    current_token.append(char)
            elif char == quote:
                if current_token:
                    yield ''.join(current_token)
                current_token = []
                quote = None
            else:
                current_token.append(char)
        if quote is not None:
            raise ValueError("No closing quotation")
        if escape:
            raise ValueError("No escaped character")
        if current_token:
            yield ''.join(current_token)

    def _gen_sentences(self, tokens):
        sentence = []
        for token in tokens:
            if token is None:
                yield sentence
                sentence = []
            else:
                sentence.append(token)
        yield sentence

    def gen_sentences(self, tokens, aliases=None):
        if aliases is None:
            aliases = {}
        for sentence in self._gen_sentences(tokens):
            if sentence[0] in aliases:
                new_tokens = Program(aliases[sentence[0]]).gen_tokens()
                sentence[0:1] = list(new_tokens)
            yield transform(Sentence(sentence), self.transforms)

    def interpret(self, sentence, environ=None):
        if environ is None:
            environ = {}
        try:
            return environ[sentence.command](*sentence.args)
        except KeyError:
            return Kernel().respond(str(sentence))

    def run(self, aliases=None, environ=None):
        tokens = self.gen_tokens()
        for sentence in self.gen_sentences(tokens, aliases):
            self.interpret(sentence, environ)
