from subprocess import check_output
import os
import readline
import sys


class Completer(object):
    def __init__(self, shell):
        self.shell = shell
        if sys.platform == 'darwin':
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.
        
        The completion should begin with 'text'.
        """
        matches = []

        head, tail = os.path.split(text)

        ls = check_output("ls %s" % head, shell=True)
        filenames = ls.split()

        for filename in filenames:
            if filename.startswith(tail):
                matches.append(os.path.join(head, filename))
        try:
            return matches[state]
        except IndexError:
            return None

    def interact(self):
        self.shell.interact()
