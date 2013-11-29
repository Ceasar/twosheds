import atexit
import os
import readline


class History(object):
    def __init__(self, shell, histfile=os.path.expanduser("~/.console-history")):
        self.shell = shell
        self.histfile = histfile
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history)

    def save_history(self):
        readline.write_history_file(self.histfile)

    def interact(self):
        self.shell.interact()
