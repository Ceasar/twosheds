import os


def cd(*args):
    """
    An argument of - is equivalent to $OLDPWD. If - is the first argument, and
    the directory change is successful, the absolute pathname of the new
    working directory is written to the standard output.
    """
    if args[0] == "-":
        try:
            newpwd, os.environ["OLDPWD"] = os.environ["OLDPWD"], os.getcwd()
        except KeyError as e:  # $OLDPWD initially not set
            raise e
        else:
            os.chdir(newpwd)
            print(newpwd)
    else:
        os.environ["OLDPWD"] = os.getcwd()
        os.chdir(*args)


def export(*args):
    for arg in args:
        k, v = arg.split("=", 1)
        os.environ[k] = v
