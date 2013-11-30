
LAST = '_'


def run_python(line, env):
    try:
        return eval(line, env, env)  # expressions
    except SyntaxError:
        exec(line, env, env)  # statements

class PythonShell(Shell):

    # TODO: Not obvious these are actually desirable

    def _raise_cursor(self, n=1):
        """Move the cursor up `n` lines."""
        self.output('\033[%sA' % n)
        sys.stdout.flush()

    def _clear_line(self):
        self.output('\033[K')
        sys.stdout.flush()

    def eval(self, line):
        if line:
            exit_code = call(line, shell=True)
            if exit_code != 0:
                # hide the error
                self._raise_cursor()
                self._clear_line()
                return run_python(line, self.env)
