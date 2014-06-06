from fixture import *


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
