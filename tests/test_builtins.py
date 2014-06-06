import os

import pytest


@pytest.mark.skipif(reason="flaky")
def test_export(shell):
    assert "X" not in os.environ
    assert "Y" not in os.environ
    shell.interpret("export X=1 Y=2")
    assert os.environ.get("X") == "1"
    assert os.environ.get("Y") == "2"
    del os.environ["X"]
    del os.environ["Y"]
