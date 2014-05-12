"""
twosheds.transform
~~~~~~~~~~~~~~~~~~

This module implements a number of grammatical transforms.

A grammatical transformation (or transformation) operates on a given
string with a given constituent structure and converts it into a new
string with a new derived constituent structure.
"""
from .sentence import Sentence


def transform(sentence, transforms, word=False, inverse=False):
    if word:
        sentence = Sentence([sentence])
    if inverse:
        transforms = reversed(transforms)
    for t in transforms:
        sentence = t(sentence, inverse)
    if word:
        return sentence.tokens[0]
    return sentence


class Transform(object):
    def __call__(self, sentence, inverse=False):
        raise NotImplementedError("Transformations must be callable.")


def is_variable(token):
    """Check if a token is a variable."""
    return token.startswith('$')


class VariableTransform(Transform):
    """Expands environmental variables.

    Variable substitutions are made in order of the length of the expansion.

    >>> env = {'HOME': '/Users/arthurjackson'}
    >>> t = VariableTransform(env)
    >>> t('cd $HOME')
    'cd /Users/arthurjackson'
    >>> t('cd /Users/arthurjackson', inverse=True)
    'cd $HOME'

    :param environment: dictionary of variables to expand
    """
    def __init__(self, environment=None):
        self.environment = environment or {}

    @property
    def _inverse_environment(self):
        # NOTE: This will be unreliable if two variables have the same value.
        return {v: k for k, v in self.environment.items()}

    def _transform(self, tokens, inverse=False):
        inverse_environment = self._inverse_environment
        if inverse:
            for token in tokens:
                try:
                    yield "$" + inverse_environment[token]
                except KeyError:
                    yield token
        else:
            for token in tokens:
                if is_variable(token):
                    yield self.environment.get(token[1:], token)
                else:
                    yield token

    def __call__(self, sentence, inverse=False):
        sentence.tokens = list(self._transform(sentence.tokens, inverse))
        return sentence


class TildeTransform(Transform):
    """
    Decorator for :class:`VariableTransform <VariableTransform>`.

    Expands ``~`` to ``$HOME``.

    >>> t = TildeTransform('/user/twosheds')
    >>> t("~")
    '/user/twosheds'
    >>> t("/user/twosheds", inverse=True)
    '~'

    """
    def __init__(self, home):
        self.home = home

    def _transform(self, sentence, inverse=False):
        TILDE = "~"
        source, target = (self.home, TILDE) if inverse else (TILDE, self.home)
        sentence.tokens = [
            token.replace(source, target) if token.startswith(source)
            else token
            for token in sentence.tokens
        ]
        return sentence

    def __call__(self, sentence, inverse=False):
        return self._transform(sentence, inverse)
