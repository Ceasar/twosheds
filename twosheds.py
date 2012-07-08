import traceback

import pbs


def cd(*args):
    pbs.cd(*args)
    print pbs.ls()


up = ".."


def run_repl(env):
    while True:
        try:
            line = raw_input("pbs> ")
        except (ValueError, EOFError):
            break
        # going to disable piping here
        tokens = line.split()
        command, args = tokens[0], tokens[1:]
        string_tokens = ('"%s"' % arg for arg in args)
        new_command = "%s(%s)" % (command, ", ".join(string_tokens))
        print new_command
        try:
            try:
                r = eval(new_command, env, env)
            except SyntaxError:
                exec(new_command, env, env)
            else:
                # Run if it's a function
                try:
                    print r()
                except:
                    if r is not None:
                        print r
        except SystemExit:
            break
        except:
            print(traceback.format_exc())

    # cleans up our last line
    print("")

EXPORTS = {
    "up": up,
    "cd": cd,
}


# we're being run as a stand-alone script, fire up a REPL
if __name__ == "__main__":
    globs = globals()

    f_globals = {}
    for k in ["__builtins__", "__doc__", "__name__", "__package__"]:
        f_globals[k] = globs[k]

    for k, v in EXPORTS.iteritems():
        f_globals[k] = v
    env = pbs.Environment(f_globals)
    run_repl(env)
