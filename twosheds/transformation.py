"""
twosheds.transformation
~~~~~~~~~~~~~~~~~~~~~~~

This module implements a number of grammatical transformations which are
used when parsing commands.

A grammatical transformation (or transformation) operates on a given
string with a given constituent structure and converts it into a new
string with a new derived constituent structure.
"""
import os

from rl import history


class Transformation(object):
    def expand(self, sentece):
        raise NotImplementedError("Transformations must implement ``expand``.")


class AliasTransformation(Transformation):
    """Expands user-defined aliases."""
    def __init__(self, aliases):
        self.aliases = aliases or {}

    def expand(self, sentence):
        """Expand aliases in a sentence.
        
        A token is a candidate for alias expansion only if it it the first
        token in a sentence.
        """
        try:
            command, args = sentence.split(" ", 1)
        except ValueError:
            command, args = sentence, ""
        try:
            return "%s %s" % (self.aliases[command], args)
        except KeyError:
            return sentence


class VariableTransformation(Transformation):
    """Expands environmental variables."""
    def expand(self, sentence):
        """Expand environmental variables in a sentence."""
        for k, v in os.environ.iteritems():
            sentence = sentence.replace("$" + k, v)
        return sentence


class TildeTransformation(Transformation):
    """Expands ``~`` to ``$HOME``"""
    def expand(self, sentence):
        return sentence.replace("~", "$HOME")


class HistoryTransformation(Transformation):
    """Performs history substitutions.

    History substitutions begins with the character ``!``.
    """

    def expand_previous(self, sentence):
        """Expand `!!` to the previous event."""
        try:
            last_command = history[-2]
        except IndexError:
            return sentence
        else:
            return sentence.replace("!!", last_command)

    def _get_number(self, word):
        chars = []
        if not word:
            raise ValueError("empty word")
        negative = (word[0] == "-")
        if negative:
            word = word[1:]
        for char in word:
            if char.isdigit():
                chars.append(char)
            else:
                break
        return int(('-' if negative else '') + ''.join(chars))

    def expand_number(self, token):
        try:
            num = self._get_number(token)
        except ValueError:
            return token
        else:
            return history[num]

    def expand_token(self, token):
        return self.expand_number(token)

    def find_tokens(self, sentence):
        tokens = sentence.split("!")
        # the first token can never begin with a ``!`` 
        for token in tokens[1:]:
            yield token

    def expand(self, sentence):
        sentence = self.expand_previous(sentence)
        for token in self.find_tokens(sentence):
            sentence = sentence.replace("!" + token, self.expand_token(token))
        return sentence
