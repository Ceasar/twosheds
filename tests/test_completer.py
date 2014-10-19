import os


class TestCompleter():
    def test_gen_filename_completions(self, completer, tmpdir):
        completer.use_suffix = False
        os.chdir(str(tmpdir))
        file1, file2, file3 = 'x', 'y z', 'README.rst'
        tmpdir.mkdir(file1)
        tmpdir.mkdir(file2)
        tmpdir.join(file3).write('')
        assert {file1, file2, file3} == set(completer.get_matches(''))
        assert {file1} == set(completer.get_matches('x'))
        assert {file2} == set(completer.get_matches('z'))
        assert set() == set(completer.get_matches('zz'))

    def test_gen_variable_completions(self, completer, environment):
        # assuming $HOME is in environment
        word = "$H"
        matches = completer.get_matches(word)
        assert matches and all(m.startswith(word) for m in matches)

    def test_gen_variable_completions_generic(self, completer, environment):
        # assuming something is in environment
        word = "$"
        matches = completer.get_matches(word)
        assert matches and all(m.startswith(word) for m in matches)

    def test_gen_variable_completions_no_match(self, completer, environment):
        # assuming $QX.* is not in environment
        word = "$QX"
        matches = completer.get_matches(word)
        assert len(matches) == 0

    def test_gen_hyphen_completions(self, completer, tmpdir):
        completer.use_suffix = False
        os.chdir(str(tmpdir))
        file1 = "a-b"
        tmpdir.mkdir(file1)
        assert file1 == completer.complete("a", 0)
        assert file1 == completer.complete("a-", 0)
        assert file1 == completer.complete("a-b", 0)
