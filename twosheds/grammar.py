

class Grammar(object):
    def __init__(self, transformations=None):
        self.transformations = transformations or []

    def lex(self, line):
        return line.replace(";", " ; ")

    def expand(self, sentence):
        """Expand any macros in a command."""
        for transformation in self.transformations:
            sentence = transformation.expand(sentence)
        return sentence

    def parse(self, source_text):
        for sentence in self.lex(source_text).split(";"):
            yield self.expand(sentence)
