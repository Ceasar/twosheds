"""
twosheds.language
~~~~~~~~~~~~~~~~~

This module implements a language, which consists of a grammar and a semantics.
"""


class Language(object):
    def __init__(self, lexicon, grammar, semantics):
        self.lexicon = lexicon
        self.grammar = grammar
        self.semantics = semantics

    def interpret(self, text):
        return self.semantics.eval(self.grammar.parse(self.lexicon.lex(text)))
