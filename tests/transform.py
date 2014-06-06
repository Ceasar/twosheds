from fixture import *


def test_variable_substitution(variable_transform):
    text = "cd $HOME"
    assert variable_transform(text) == "cd %s" % HOME


def test_variable_substitution_inverse(variable_transform):
    text = "cd %s" % HOME
    assert variable_transform(text, inverse=True) == "cd $HOME"


def test_variable_substitution_only_at_start(variable_transform):
    """
    Expansion of variables should only happen if token starts with a variable.

    Thus, assuming "$EDITOR" is a variable, "$EDITOR" should be expanded, but "x$EDITOR" should not.
    
    Thus if "EDITOR=vim", expansion of "xvim" should do nothing,
    not replace with 'f$EDITOR'.
    """
    text = 'x$EDITOR'
    assert variable_transform(text) == text
    text = 'x%s' % EDITOR
    assert variable_transform(text, inverse=True) == text

def test_variable_substitution_order(variable_transform):
    """Variable substitution should substitute longer values first."""
    text = "cd %s" % HOME
    assert variable_transform(text, inverse=True) == "cd $HOME"


def test_variable_substitution_id(variable_transform):
    text = "$HOME"
    assert variable_transform(variable_transform(text), inverse=True) == text


def test_tilde_substitution1(tilde_transform, environment):
    """Tilde substitution should expand ``~`` as ``$HOME``."""
    text = "cd ~"
    assert tilde_transform(text) == "cd %s" % environment['HOME']
    text = "cd ~/Desktop"
    assert tilde_transform(text) == "cd %s/Desktop" % environment['HOME']


def test_tilde_substitution2(tilde_transform):
    """
    Tilde substitution should not expand a tilde unless it is the prefix
    of a token.
    """
    text = "git rebase -i HEAD~3"
    assert tilde_transform(text) == text


def test_tilde_substitution_inverse(tilde_transform):
    """Tilde substitution should have an inverse."""
    text = "~"
    assert tilde_transform(tilde_transform(text), inverse=True) == text


def test_transform(transforms):
    text = "home"
    assert transform(text, transforms) == "cd %s" % HOME


def test_transform_inverse(transforms):
    text = "cd %s" % HOME
    assert transform(text, transforms, inverse=True) == "home"


def test_transform_id(transforms):
    text = "home"
    actual = transform(transform(text, transforms), transforms, inverse=True)
    assert actual == text
