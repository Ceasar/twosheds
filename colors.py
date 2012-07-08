

# green
_SUCCESS = '\033[92m'
# yellow
_WARNING = '\033[93m'
# red
_FAIL = '\033[91m'
# no color
_ENDC = '\033[0m'


def success(text):
    """Color text to indicate success."""
    return "%s%s%s" % (_SUCCESS, text, _ENDC)


def warn(text):
    """Color text to indicate a warning."""
    return "%s%s%s" % (_WARNING, text, _ENDC)


def fail(text):
    """Color text to indicate a failure."""
    return "%s%s%s" % (_FAIL, text, _ENDC)
