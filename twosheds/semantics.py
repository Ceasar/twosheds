"""
twosheds.semantics
~~~~~~~~~~~~~~~~~~

This module implements a semantics for user inputs. It is responsible for
evaluating user inputs in the kernel language.
"""
import os
import shlex
import subprocess


def cd(*args):
    os.chdir(*args)


def export(*args):
    for arg in args:
        k, v = arg.split("=", 1)
        os.environ[k] = v


class Semantics(object):
    BUILTINS = {
        'cd': cd,
        'export': export,
    }

    def __init__(self, builtins=None):
        self.builtins = builtins or self.BUILTINS

    def eval_sentence(self, sentence):
        """Evaluate a single command."""
        if not sentence:
            return
        tokens = shlex.split(sentence)
        command, args = tokens[0], tokens[1:]
        try:
            self.builtins[command](*args)
        except KeyError:
            process = subprocess.Popen(sentence, shell=True)
            process.communicate()

    def eval(self, sentences):
        """Evaluate a sequence of commands."""
        for sentence in sentences:
            self.eval_sentence(sentence)
