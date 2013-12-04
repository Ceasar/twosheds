"""
twosheds.grammar
~~~~~~~~~~~~~~~~

This module implements a grammar for user inputs. It is responsible for
converting user inputs into the kernel language and supplying sentences for
evaluation.
"""


class Grammar(object):
    def __init__(self, echo=False, transforms=None):
        self.echo = echo
        self.transforms = transforms or []

    def lex(self, text):
        return text.replace(";", " ; ")

    def transform(self, sentence, inverse=False):
        """Rewrite a sentence to a kernel sentence."""
        transforms = reversed(self.transforms) if inverse else self.transforms
        for transform in transforms:
            sentence = transform(sentence, inverse)
        return sentence

    def parse(self, source_text):
        sentences = self.lex(source_text).split(";")
        for sentence in sentences:
            transformation = self.transform(sentence)
            if self.echo:
                print transformation
            yield transformation
