import os
import subprocess


class Interpreter(object):
    BUILTINS = {'cd': os.chdir}

    def __init__(self, grammar, builtins=None):
        self.grammar = grammar
        self.builtins = builtins or self.BUILTINS

    def run(self, source_text):
        self.eval(self.grammar.parse(source_text))

    def eval_one(self, line):
        """Evaluate a single command."""
        if not line:
            return
        tokens = line.split()
        command, args = tokens[0], tokens[1:]
        try:
            self.builtins[command](*args)
        except KeyError:
            subprocess.call(line, shell=True)

    def eval(self, lines):
        """Evaluate a sequence of commands."""
        for line in lines:
            self.eval_one(line)
