import pytest

from twosheds import Shell
from twosheds.grammar import Grammar
from twosheds.transform import (AliasTransform,
                                VariableTransform,
                                TildeTransform,)


@pytest.fixture
def aliases():
    return {
        "ls": "ls -G",
        "home": "cd ~",
    }


@pytest.fixture
def environment():
    return {
        "HOME": "/user/twosheds",
        "LOGNAME": "twosheds",
    }


@pytest.fixture
def alias_transform(aliases):
    return AliasTransform(aliases)


@pytest.fixture
def variable_transform(environment):
    return VariableTransform(environment)


@pytest.fixture
def tilde_transform():
    return TildeTransform()


@pytest.fixture
def grammar(alias_transform, tilde_transform, variable_transform):
    transforms = [
        alias_transform,
        tilde_transform,
        variable_transform,
    ]
    return Grammar(transforms=transforms)


@pytest.fixture
def shell():
    return Shell()


def test_shell(shell):
    assert shell.eval("echo") == 0

def test_alias_substitution1(alias_transform):
    """Alias substitution should expand aliases."""
    text = "ls"
    assert alias_transform(text) == "ls -G"


def test_alias_substitution2(alias_transform):
    """Alias substitution should not expand arguments."""
    text = "echo ls"
    assert alias_transform(text) == text


def test_alias_substitution_inverse(alias_transform):
    """Alias substitution should have an inverse."""
    text = "ls"
    assert alias_transform(alias_transform(text), inverse=True) == text


def test_variable_substitution(variable_transform):
    text = "cd $HOME"
    assert variable_transform(text) == "cd /user/twosheds"


def test_variable_substitution_inverse(variable_transform):
    text = "cd /user/twosheds"
    assert variable_transform(text, inverse=True) == "cd $HOME"


def test_variable_substitution_order(variable_transform):
    """Variable substitution should substitute longer values first."""
    text = "cd /user/twosheds"
    assert variable_transform(text, inverse=True) == "cd $HOME"


def test_variable_substitution_id(variable_transform):
    text = "$HOME"
    assert variable_transform(variable_transform(text), inverse=True) == text


def test_tilde_substitution1(tilde_transform):
    """Tilde substitution should expand ``~`` as ``$HOME``."""
    text = "cd ~/Desktop"
    assert tilde_transform(text) == "cd $HOME/Desktop"


def test_tilde_substitution2(tilde_transform):
    """
    Tilde substitution should not expand a tilde unless it is the prefix
    of a token.
    """
    text = "git rebase -i HEAD~3"
    assert tilde_transform(text) == text


def test_tilde_substitution_inverse(tilde_transform):
    """Tilde substitution should have an inverse."""
    text = "cd ~/Desktop"
    assert tilde_transform(tilde_transform(text), inverse=True) == text


def test_grammar_transform(grammar):
    text = "home"
    assert grammar.transform(text) == "cd /user/twosheds"


def test_grammar_transform_inverse(grammar):
    text = "cd /user/twosheds"
    assert grammar.transform(text, inverse=True) == "home"


def test_grammar_transform_id(grammar):
    text = "home"
    assert grammar.transform(grammar.transform(text), inverse=True) == text
