import traceback

# this is the same as sh, except it allows foreground
import pbs
import sh
from pycolorterm.pycolorterm import pretty_output, styles
from sh import CommandNotFound


LAST = '_'

def get_prompt():
    return "$ "


def run_command(line, env):
    tokens = line.split()
    command, args = tokens[0].replace("-", "_"), tokens[1:]
    string_tokens = [arg if arg in env else '"%s"' % arg for arg in args]
    if args:
        if args[-1] == "&":
            string_tokens[-1] = "_bg=True"
        elif args[-1] == "!":
            env = pbs.Environment()
            string_tokens[-1] = "_fg=True"
    new_command = "%s(%s)" % (command, ", ".join(string_tokens))
    # TODO: Log this properly
    # print new_command
    env[LAST] = rv = eval(new_command, env, env)
    try:
        return rv.strip()
    except:
        return rv


def run_python(line, env):
    try:
        env[LAST] = rv = eval(line, env, env)  # expressions
        return rv
    except SyntaxError:
        exec(line, env, env)  # statements


def main(env):
    while True:
        try:
            line = raw_input(get_prompt())
        except (ValueError, EOFError):
            break
        if not line:
            continue
        try:
            try:
                rv = run_command(line, env)
            except:
                rv = run_python(line, env)
        except SystemExit:
            break
        except:
            with pretty_output(styles['FG_RED']) as out:
                out.write(traceback.format_exc())
        else:
            print rv

if __name__ == "__main__":
    # this allows lookups to names that aren't found in the global scope to be
    # searched for as a program name.  for example, if "ls" isn't found in this
	# module's scope, we consider it a system program and try to find it.
    env = sh.Environment({})
    main(env)
