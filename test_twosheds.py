from twosheds.transformation import (AliasTransformation,
                                     VariableTransformation,
                                     TildeTransformation,)


def test_alias_substitution1():
    """Alias substitution should expand aliases."""
    aliases = {"ls": "ls -G"}
    transformation = AliasTransformation(aliases)
    text = "ls"
    assert transformation.decode(text) == "ls -G"


def test_alias_substitution2():
    """Alias substitution should not expand arguments."""
    aliases = {"ls": "ls -G"}
    transformation = AliasTransformation(aliases)
    text = "echo ls"
    assert transformation.decode(text) == "echo ls"


def test_alias_substitution_inverse():
    """Alias substitution should have an inverse."""
    aliases = {"ls": "ls -G"}
    transformation = AliasTransformation(aliases)
    text = "ls"
    assert transformation.encode(transformation.decode(text)) == text


def test_variable_substitution_inverse():
    environment = {"$HOME": "/user/twosheds"}
    transformation = VariableTransformation(environment)
    text = "$"
    assert transformation.encode(transformation.decode(text)) == text


def test_tilde_substitution1():
    """Tilde substitution should expand ``~`` as ``$HOME``."""
    transformation = TildeTransformation()
    text = "cd ~/Desktop"
    assert transformation.decode(text) == "cd $HOME/Desktop"


def test_tilde_substitution2():
    """
    Tilde substitution should not expand a tilde unless it is the prefix
    of a token.
    """
    transformation = TildeTransformation()
    text = "git rebase -i HEAD~3"
    assert transformation.decode(text) == text


def test_tilde_substitution_inverse():
    """Tilde substitution should have an inverse."""
    transformation = TildeTransformation()
    text = "cd ~/Desktop"
    assert transformation.encode(transformation.decode(text)) == text
