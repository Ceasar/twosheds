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

    def transform(self, sentence, inverse=False):
        """Rewrite a sentence to a kernel sentence."""
        transforms = reversed(self.transforms) if inverse else self.transforms
        for transform in transforms:
            sentence = transform(sentence, inverse)
        return sentence

    def _gen_sentences(self, tokens):
        sentence = []
        for token in tokens:
            if token == ";":
                yield sentence
                sentence = []
            else:
                sentence.append(token)
        yield sentence

    def parse(self, tokens):
        sentences = self._gen_sentences(tokens)
        for sentence in sentences:
            transformation = self.transform(" ".join(sentence))
            if self.echo:
                print transformation
            yield transformation
