"""
twosheds.transform
~~~~~~~~~~~~~~~~~~

This module implements a number of grammatical transforms.

A grammatical transformation (or transformation) operates on a given
string with a given constituent structure and converts it into a new
string with a new derived constituent structure.
"""


class Transform(object):
    def __call__(self, sentence, inverse=False):
        raise NotImplementedError("Transformations must be callable.")


class AliasTransform(Transform):
    """
    Expands user-defined aliases.

    >>> aliases = {'ls': 'ls -G'}
    >>> t = AliasTransform(aliases)
    >>> t('ls')
    'ls -G'
    >>> t('ls -G', inverse=True)
    'ls'

    A token is a candidate for alias expansion only if it is a command.

    >>> t('echo ls')  # no effect
    'echo ls'

    :param aliases: dictionary of aliases to expand
    """
    def __init__(self, aliases=None):
        self.aliases = aliases or {}

    def __call__(self, sentence, inverse=False):
        if inverse:
            for k, v in self.aliases.iteritems():
                if sentence.startswith(v):
                    sentence = sentence.replace(v, k)
                    break
            return sentence
        else:
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
        tokens = sentence.split()
        return " ".join(self._transform(tokens, inverse))


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
        tokens = sentence.split()
        TILDE = "~"
        source, target = (self.home, TILDE) if inverse else (TILDE, self.home)
        return " ".join(
            token.replace(source, target) if token.startswith(source)
            else token
            for token in tokens
        )

    def __call__(self, sentence, inverse=False):
        return self._transform(sentence, inverse)
