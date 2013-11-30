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
