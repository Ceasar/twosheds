"""

    twosheds.completer
    ~~~~~~~~~~~~~~~~~~

    This module implements command completion.

"""
import os
import readline
import sys


class Completer(object):
    """A completer completes words when given a unique abbreviation.
    
    Type part of a word (for example `ls /usr/lost') and hit the tab key to
    run the completer.
    
    The shell completes the filename `/usr/lost' to `/usr/lost+found/',
    replacing the incomplete word with the complete word in the input buffer.
    
    (Note the terminal `/'; completion adds a `/' to the end of completed
    directories and a space to the end of other completed words, to speed
    typing and provide a visual indicator of successful completion.
    Completer.use_suffix can be set False to prevent this.)
    
    If no match is found (perhaps `/usr/lost+found' doesn't exist), then no
    matches will appear.
    
    If the word is already complete (perhaps there is a `/usr/lost' on your
    system, or perhaps you were thinking too far ahead and typed the whole
    thing) a `/' or space is added to the end if it isn't already there.
    """
    def __init__(self, shell, use_suffix=True):
        self.shell = shell
        self.use_suffix = use_suffix
        if sys.platform == 'darwin':
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)

    def inflect(self, filename):
        """Inflect a filename to indicate its type.

        If the file is a directory, the suffix "/" is appended, otherwise
        a space is appended.
        """
        return filename + ("/" if os.path.isdir(filename) else " ")

    def get_matches(self, text):
        """Find all files that match `word`."""
        head, tail = os.path.split(text)

        filenames = os.listdir(head or '.')

        if tail:
            return [os.path.join(head, filename) for filename in filenames
                    if filename.startswith(tail)]
        else:
            # do not show hidden files when listing contents of a directory
            return [os.path.join(head, filename) for filename in filenames
                    if not filename.startswith('.')]

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        This is called successively with state == 0, 1, 2, ... until it
        returns None.
        
        The completion should begin with 'text'.
        """
        matches = self.get_matches(text)
        if self.use_suffix:
            matches = [self.inflect(match) for match in matches]
        try:
            return matches[state]
        except IndexError:
            return None

    def interact(self, banner=None):
        self.shell.interact(banner)
