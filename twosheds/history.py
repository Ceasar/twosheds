import atexit
import os
import readline


DEFAULT_HISTFILE = os.path.expanduser("~/.console-history")

class History(object):
    def __init__(self, histfile=DEFAULT_HISTFILE):
        self.histfile = histfile
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history)

    def save_history(self):
        readline.write_history_file(self.histfile)
