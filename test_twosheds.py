from twosheds.grammar import Grammar
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


def test_variable_substitution():
    environment = {"HOME": "/user/twosheds"}
    transformation = VariableTransform(environment)
    text = "cd $HOME"
    assert transformation(text) == "cd /user/twosheds"


def test_variable_substitution_inverse():
    environment = {"HOME": "/user/twosheds"}
    transformation = VariableTransform(environment)
    text = "cd /user/twosheds"
    assert transformation(text, inverse=True) == "cd $HOME"


def test_variable_substitution_order():
    """Variable substitution should substitute longer values first."""
    environment = {
        "HOME": "/user/twosheds",
        "LOGNAME": "twosheds",
    }
    transformation = VariableTransform(environment)
    text = "cd /user/twosheds"
    assert transformation(text, inverse=True) == "cd $HOME"


def test_variable_substitution_id():
    environment = {"HOME": "/user/twosheds"}
    transformation = VariableTransform(environment)
    text = "$HOME"
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


def test_grammar_expand_transform():
    aliases = {"home": "cd ~"}
    environment = {"HOME": "/user/twosheds"}
    transforms = [
        AliasTransform(aliases),
        TildeTransform(),
        VariableTransform(environment),
    ]
    text = "home"
    grammar = Grammar(transforms=transforms)
    assert grammar.transform(text) == "cd /user/twosheds"


def test_grammar_expand_inverse():
    aliases = {"home": "cd ~"}
    environment = {"HOME": "/user/twosheds"}
    transforms = [
        AliasTransform(aliases),
        TildeTransform(),
        VariableTransform(environment),
    ]
    text = "cd /user/twosheds"
    grammar = Grammar(transforms=transforms)
    assert grammar.transform(text, inverse=True) == "home"


def test_grammar_expand_id():
    aliases = {"home": "cd ~"}
    environment = {"HOME": "/user/twosheds"}
    transforms = [
        AliasTransform(aliases),
        TildeTransform(),
        VariableTransform(environment),
    ]
    text = "home"
    grammar = Grammar(transforms=transforms)
    assert grammar.transform(grammar.transform(text), inverse=True) == text
