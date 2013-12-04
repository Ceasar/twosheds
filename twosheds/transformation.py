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
    def encode(self, sentence):
        """Transform a sentence toward a surface sentence."""
        raise NotImplementedError("Transformations must implement ``decode``.")

    def decode(self, sentence):
        """Transform a sentence toward a kernel sentence."""
        raise NotImplementedError("Transformations must implement ``decode``.")


class AliasTransformation(Transformation):
    """
    Expands user-defined aliases.

    A token is a candidate for alias expansion only if it it the first
    token in a sentence.

    :param aliases: dictionary of aliases to expand
    """
    def __init__(self, aliases):
        self.aliases = aliases or {}

    def encode(self, sentence):
        for k, v in self.aliases.iteritems():
            if sentence.startswith(v):
                sentence = sentence.replace(v, k)
                break
        return sentence

    def decode(self, sentence):
        try:
            command, args = sentence.split(" ", 1)
        except ValueError:
            command, args = sentence, ""
        try:
            if args:
                return "%s %s" % (self.aliases[command], args)
            else:
                return "%s" % (self.aliases[command],)
        except KeyError:
            return sentence


class VariableTransformation(Transformation):
    """Expands environmental variables.
    
    :param environment: dictionary of variables to expand
    """
    def __init__(self, environment=None):
        self.environment = environment or {}

    def encode(self, sentence):
        for k, v in self.environment.iteritems():
            if v in sentence:
                return sentence.replace(v, "$" + k)
        return sentence

    def decode(self, sentence):
        """Expand environmental variables in a sentence."""
        for k, v in self.environment.iteritems():
            sentence = sentence.replace("$" + k, v)
        return sentence


class TildeTransformation(Transformation):
    """Expands ``~`` to ``$HOME``"""

    def encode(self, sentence):
        tokens = sentence.split()
        return " ".join((token.replace("$HOME", "~") if token.startswith("$HOME")
                        else token) for token in tokens)

    def decode(self, sentence):
        tokens = sentence.split()
        return " ".join((token.replace("~", "$HOME") if token.startswith("~")
                         else token) for token in tokens)
