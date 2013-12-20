"""
twosheds.completer
~~~~~~~~~~~~~~~~~~

This module implements command completion.
"""
import os
import re
import rl
import sys
import traceback


class Completer(object):
    """A Completer completes words when given a unique abbreviation.
    
    Type part of a word (for example ``ls /usr/lost``) and hit the tab key to
    run the completer.
    
    The shell completes the filename ``/usr/lost`` to ``/usr/lost+found/``,
    replacing the incomplete word with the complete word in the input buffer.

    .. note::
    
        Completion adds a ``/`` to the end of completed directories and a
        space to the end of other completed words, to speed typing and provide
        a visual indicator of successful completion. Completer.use_suffix can be set ``False`` to prevent this.
    
    If no match is found (perhaps ``/usr/lost+found`` doesn't exist), then no
    matches will appear.
    
    If the word is already complete (perhaps there is a ``/usr/lost`` on your
    system, or perhaps you were thinking too far ahead and typed the whole
    thing) a ``/`` or space is added to the end if it isn't already there.

    The shell will list the remaining choices (if any) below the unfinished
    command line whenever completion fails, for example::

        $ ls /usr/l[tab]
        lbin/       lib/        local/      lost+found/

    Completion will always happen on the shortest possible unique match, even
    if more typing might result in a longer match. Therefore::

        $ ls
        fodder   foo      food     foonly
        $ rm fo[tab]

    just beeps, because ``fo`` could expand to ``fod`` or ``foo``, but if we
    type another ``o``::

        $ rm foo[tab]
        $ rm foo

    the completion completes on ``foo``, even though ``food`` and ``foonly``
    also match.

    .. note::
        
        ``excludes_patterns`` can be set to a list of regular expression
        patterns to be ignored by completion.
        
        Consider that the completer were initialized to ignore
        ``[r'.*~', r'.*.o']``::

            $ ls
            Makefile        condiments.h~   main.o          side.c
            README          main.c          meal            side.o
            condiments.h    main.c~
            $ emacs ma[tab]
            main.c

    :param grammar: A :class:`Grammar <grammar.Grammar>` to expand aliases.
    :param use_suffix: add a ``/`` to completed directories and a space to the
                       end of other completed words, to speed typing and
                       provide a visual indicator of successful completion.
                       Defaults to ``True``.
    :param excludes: a list of regular expression patterns to be ignored by
                     completion. 
    """
    def __init__(self, grammar, use_suffix=True, exclude=None):
        self.grammar = grammar
        self.use_suffix = use_suffix
        self.exclude_patterns = exclude or []

    def complete(self, word, state):
        """Return the next possible completion for ``word``.

        This is called successively with ``state == 0, 1, 2, ...`` until it
        returns ``None``.
        
        The completion should begin with ``word``.

        :param word: the word to complete
        :param state: an int, used to iterate over the choices
        """
        # expand the line buffer before completing
        rl.completion.line_buffer = self.grammar.expand(rl.completion.line_buffer)

        # TODO: doing this manually right now, but may make sense to exploit
        rl.completion.suppress_append = True
        # rl.completion.filename_completion_desired = True

        rl.completer.word_break_characters = (rl.completer
                                              .word_break_characters
                                              .replace("$", "")
                                              .replace("/", ""))

        matches = self.gen_matches(word)
        # defend this against bad user input for regular expression patterns
        try:
            matches = self.exclude_matches(matches)
        except:
            sys.stderr.write(traceback.format_exc())
        if self.use_suffix:
            matches = [self.inflect(match) for match in matches]
        try:
            return list(matches)[state]
        except IndexError:
            return None

    def exclude_matches(self, matches):
        """Filter any matches that match an exclude pattern.

        :param matches: a list of possible completions
        """
        for match in matches:
            for exclude_pattern in self.exclude_patterns:
                if re.match(exclude_pattern, match) is not None:
                    break
            else:
                yield match

    def _is_hidden_file(self, filename):
        return filename.startswith('.')

    def gen_filename_completions(self, word, filenames):
        """Generate a sequence of filenames that match ``word``.
        
        :param word: the word to complete
        """
        if word:
            for filename in filenames:
                if filename.startswith(word):
                    yield filename
        else:
            for filename in filenames:
                if not self._is_hidden_file(filename):
                    yield filename
        # return results that match anywhere in the file if no results are
        # found
        if not matches:
            for filename in filenames:
                if word in filename:
                    yield filename

    def gen_matches(self, word):
        """Generate a sequence of possible completions for ``word``.
        
        :param word: the word to complete
        """

        if word.startswith("$"):
            for match in self.gen_variable_completions(word, os.environ):
                yield match
        else:
            head, tail = os.path.split(word)
            filenames = os.listdir(head or '.')
            for match in self.gen_filename_completions(tail, filenames):
                yield os.path.join(head, match)

    def gen_variable_completions(self, word, env):
        """Generate a sequence of possible variable completions for ``word``.
        
        :param word: the word to complete
        :param env: the environment
        """ 
        var = word[1:]
        for k in env:
            if k.startswith(var):
                yield "$" + k

    def inflect(self, filename):
        """Inflect a filename to indicate its type.

        If the file is a directory, the suffix "/" is appended, otherwise
        a space is appended.

        :param filename: the name of the file to inflect
        """
        return filename + ("/" if os.path.isdir(filename) else " ")
