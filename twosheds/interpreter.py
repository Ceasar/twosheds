import os
import subprocess


class Interpreter(object):
    BUILTINS = {'cd': os.chdir}

    def __init__(self, aliases=None, builtins=None):
        self.aliases = aliases or {}
        self.builtins = builtins or self.BUILTINS

    def run(self, source_text):
        self.eval(self.lex(source_text).split(";"))

    def lex(self, line):
        return line.replace(";", " ; ")

    def expand_aliases(self, line):
        """Expand aliases in a line."""
        try:
            command, args = line.split(" ", 1)
        except ValueError:
            command, args = line, ""
        try:
            return "%s %s" % (self.aliases[command], args)
        except KeyError:
            return line

    def expand_variables(self, line):
        """Expand environmental variables in a line."""
        tokens = line.split()
        new_tokens = []
        for token in tokens:
            if token.startswith("$"):
                try:
                    token = os.environ[token[1:]]
                except KeyError:
                    pass
            new_tokens.append(token)
        return " ".join(new_tokens)

    def expand(self, line):
        """Expand any macros in a command."""
        return self.expand_variables(self.expand_aliases(line))

    def eval_one(self, line):
        """Evaluate a single command."""
        if not line:
            return
        tokens = self.expand(line).split()
        command, args = tokens[0], tokens[1:]
        try:
            self.builtins[command](*args)
        except KeyError:
            subprocess.call(line, shell=True)

    def eval(self, lines):
        """Evaluate a sequence of commands."""
        for line in lines:
            self.eval_one(line)
