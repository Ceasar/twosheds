"""
twosheds.grammar
~~~~~~~~~~~~~~~~

This module implements a grammar for user inputs. It is responsible for
converting user inputs into the kernel language and supplying sentences for
evaluation.
"""

class Grammar(object):
    def __init__(self, transformations=None):
        self.transformations = transformations or []

    def lex(self, text):
        return text.replace(";", " ; ")

    def expand(self, sentence):
        """Rewrite a sentence to make it suitable for evaluation."""
        for transformation in self.transformations:
            sentence = transformation.expand(sentence)
        return sentence

    def parse(self, source_text):
        sentences = self.lex(source_text).split(";")
        for sentence in sentences:
            yield self.expand(sentence)
