import os


def cd(*args):
    if args[0] == "-":
        try:
            (newpwd, os.environ["OLDPWD"]) = (os.environ["OLDPWD"], os.getcwd())
            os.chdir(newpwd)
        except KeyError: # $OLDPWD initially not set
            newpwd = os.environ["OLDPWD"] = os.getcwd()
        print newpwd
    else:
        os.environ["OLDPWD"] = os.getcwd()
        os.chdir(*args)


def export(*args):
    for arg in args:
        k, v = arg.split("=", 1)
        os.environ[k] = v
