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

    def __call__(self, sentence, inverse=False):
        env_vars = self.environment.items()
        env_vars.sort(key=lambda (_, v): len(v), reverse=True)
        if inverse:
            for k, v in env_vars:
                if v in sentence:
                    return sentence.replace(v, "$" + k)
        else:
            for k, v in env_vars:
                sentence = sentence.replace("$" + k, v)
        return sentence


class TildeTransform(Transform):
    """
    Decorator for :class:`VariableTransform <VariableTransform>`.
    
    Expands ``~`` to ``$HOME``.

    >>> t = TildeTransform(lambda s, i: s)
    >>> t("~")
    '$HOME'
    >>> t("$HOME", inverse=True)
    '~'

    :param variable_transform: the :class:`VariableTransform <VariableTransform>`
                               to decorate
    """
    def __init__(self, variable_transform):
        self.variable_transform = variable_transform

    def _transform(self, sentence, inverse=False):
        tokens = sentence.split()
        TILDE = "~"
        HOME = "$HOME"
        source, target = (HOME, TILDE) if inverse else (TILDE, HOME)
        return " ".join(
            token.replace(source, target) if token.startswith(source)
            else token
            for token in tokens
        )

    def __call__(self, sentence, inverse=False):
        if inverse:
            replacement = self.variable_transform(sentence, inverse)
            return self._transform(replacement, inverse)
        else:
            replacement = self._transform(sentence, inverse)
            return self.variable_transform(replacement, inverse)
