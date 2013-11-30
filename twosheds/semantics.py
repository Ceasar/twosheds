"""
twosheds.semantics
~~~~~~~~~~~~~~~~~~

This module implements a semantics for user inputs. It is responsible for
evaluating user inputs in the kernel language.
"""
import os
import subprocess


class Semantics(object):
    BUILTINS = {'cd': os.chdir}

    def __init__(self, builtins=None):
        self.builtins = builtins or self.BUILTINS

    def eval_sentence(self, sentence):
        """Evaluate a single command."""
        if not sentence:
            return
        tokens = sentence.split()
        command, args = tokens[0], tokens[1:]
        try:
            self.builtins[command](*args)
        except KeyError:
            subprocess.call(sentence, shell=True)

    def eval(self, sentences):
        """Evaluate a sequence of commands."""
        for sentence in sentences:
            self.eval_sentence(sentence)
