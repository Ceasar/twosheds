import os

import pytest

import sys
sys.path.insert(0, os.path.abspath('..'))

from twosheds import Shell
from twosheds.completer import Completer
from twosheds.transform import VariableTransform, TildeTransform


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
def environment():
    return {
        "EDITOR": EDITOR,
        "HOME": HOME,
        "LOGNAME": LOGNAME,
    }


@pytest.fixture
def shell():
    return Shell()


@pytest.fixture
def variable_transform(environment):
    return VariableTransform(environment)


@pytest.fixture
def tilde_transform(environment):
    return TildeTransform(environment['HOME'])


@pytest.fixture
def transforms(variable_transform, tilde_transform):
    return [variable_transform, tilde_transform]


@pytest.fixture
def completer(transforms):
    return Completer(transforms)
