import os


def cd(*args):
    os.chdir(*args)


def export(*args):
    for arg in args:
        k, v = arg.split("=", 1)
        os.environ[k] = v
