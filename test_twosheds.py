from twosheds.transformation import TildeTransformation


def test_tilde_substitution1():
    """Ensure tilde substitution substitutes $HOME."""
    transformation = TildeTransformation()
    text = "cd ~/Desktop"
    assert transformation.expand(text) == "cd $HOME/Desktop"


def test_tilde_substitution2():
    """
    Ensure tilde substitution does not substitutes unless ``~`` is at start of
    token.
    """
    transformation = TildeTransformation()
    text = "git rebase -i HEAD~3"
    assert transformation.expand(text) == text
