# - *- coding:utf-8 -*-
"""
twosheds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

twosheds is a libary, wirten in Python, for making command language
interpreters, or shells.

"""
from __future__ import absolute_import

from .shell import Shell  # noqa
from .sentence import Sentence  # noqa
from .transform import transform  # noqa

__version_info__ = ('0', '1', '2')
__version__ = '.'.join(__version_info__)
