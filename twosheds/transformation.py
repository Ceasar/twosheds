import os


class AliasTransformation(object):
    def __init__(self, aliases):
        self.aliases = aliases or {}

    def expand(self, sentence):
        """Expand aliases in a sentence."""
        try:
            command, args = sentence.split(" ", 1)
        except ValueError:
            command, args = sentence, ""
        try:
            return "%s %s" % (self.aliases[command], args)
        except KeyError:
            return sentence


class VariableTransformation(object):

    def expand(self, sentence):
        """Expand environmental variables in a sentence."""
        tokens = sentence.split()
        new_tokens = []
        for token in tokens:
            if token.startswith("$"):
                try:
                    token = os.environ[token[1:]]
                except KeyError:
                    pass
            new_tokens.append(token)
        return " ".join(new_tokens)
