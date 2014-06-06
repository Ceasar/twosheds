

class Sentence(object):
    def __init__(self, tokens):
        self.tokens = tokens

    @property
    def command(self):
        return str(self.tokens[0])

    @property
    def args(self):
        return [str(t) for t in self.tokens[1:]]

    def __str__(self):
        return " ".join(str(token) for token in self.tokens)

    def __repr__(self):
        return "Sentence(%s)" % self.tokens
