from twosheds.transform import (AliasTransform,
                                VariableTransform,
                                TildeTransform,)


def test_alias_substitution1():
    """Alias substitution should expand aliases."""
    aliases = {"ls": "ls -G"}
    transformation = AliasTransform(aliases)
    text = "ls"
    assert transformation(text) == "ls -G"


def test_alias_substitution2():
    """Alias substitution should not expand arguments."""
    aliases = {"ls": "ls -G"}
    transformation = AliasTransform(aliases)
    text = "echo ls"
    assert transformation(text) == "echo ls"


def test_alias_substitution_inverse():
    """Alias substitution should have an inverse."""
    aliases = {"ls": "ls -G"}
    transformation = AliasTransform(aliases)
    text = "ls"
    assert transformation(transformation(text), inverse=True) == text


def test_variable_substitution_inverse():
    environment = {"$HOME": "/user/twosheds"}
    transformation = VariableTransform(environment)
    text = "$"
    assert transformation(transformation(text), inverse=True) == text


def test_tilde_substitution1():
    """Tilde substitution should expand ``~`` as ``$HOME``."""
    transformation = TildeTransform()
    text = "cd ~/Desktop"
    assert transformation(text) == "cd $HOME/Desktop"


def test_tilde_substitution2():
    """
    Tilde substitution should not expand a tilde unless it is the prefix
    of a token.
    """
    transformation = TildeTransform()
    text = "git rebase -i HEAD~3"
    assert transformation(text) == text


def test_tilde_substitution_inverse():
    """Tilde substitution should have an inverse."""
    transformation = TildeTransform()
    text = "cd ~/Desktop"
    assert transformation(transformation(text), inverse=True) == text
