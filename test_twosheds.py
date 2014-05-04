import os

import pytest

from twosheds import Shell
from twosheds.completer import Completer
from twosheds.transform import (transform,
                                AliasTransform,
                                VariableTransform,
                                TildeTransform,)

EDITOR = "vim"
HOME = os.environ['HOME']
LOGNAME = os.environ['LOGNAME']


@pytest.fixture
def aliases():
    return {
        "ls": "ls -G",
        "home": "cd ~",
    }


@pytest.fixture
def completer(transforms):
    return Completer(transforms)


@pytest.fixture
def environment():
    return {
        "EDITOR": EDITOR,
        "HOME": HOME,
        "LOGNAME": LOGNAME,
    }


@pytest.fixture
def alias_transform(aliases):
    return AliasTransform(aliases)


@pytest.fixture
def variable_transform(environment):
    return VariableTransform(environment)


@pytest.fixture
def tilde_transform(environment):
    return TildeTransform(environment['HOME'])


@pytest.fixture
def transforms(alias_transform, variable_transform, tilde_transform):
    return [alias_transform, variable_transform, tilde_transform]


@pytest.fixture
def shell():
    return Shell()


def test_shell(shell):
    assert shell.eval("echo") is None


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


@pytest.mark.skipif(reason="flaky")
def test_export(shell):
    assert "X" not in os.environ
    assert "Y" not in os.environ
    shell.interpret("export X=1 Y=2")
    assert os.environ.get("X") == "1"
    assert os.environ.get("Y") == "2"
    del os.environ["X"]
    del os.environ["Y"]


class TestCompleter():
    def test_gen_filename_completions(self, completer, tmpdir):
        os.chdir(str(tmpdir))
        tmpdir.join('README.rst').write('')
        tmpdir.mkdir('dev')
        tmpdir.mkdir('foo bar')
        matches = completer.get_matches('')
        assert ['dev/', 'foo\\ bar/', 'README.rst '] == matches
        matches = completer.get_matches('d')
        assert ['dev/'] == matches
        matches = completer.get_matches('bar')
        assert ['foo\\ bar/'] == matches
        matches = completer.get_matches('z')
        assert [] == matches

    def test_gen_variable_completions(self, completer, environment):
        # assuming $HOME is in environment
        word = "$H"
        matches = completer.get_matches(word)
        assert matches and all(m.startswith(word) for m in matches)

    def test_gen_variable_completions_generic(self, completer, environment):
        # assuming something is in environment
        word = "$"
        matches = completer.get_matches(word)
        assert matches and all(m.startswith(word) for m in matches)

    def test_gen_variable_completions_no_match(self, completer, environment):
        # assuming $QX.* is not in environment
        word = "$QX"
        matches = completer.get_matches(word)
        assert len(matches) == 0
