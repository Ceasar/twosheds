import shlex


class Request(object):
    def __init__(self, text):
        self.text = text

    @property
    def tokens(self):
        return shlex.split(self.text)

    @property
    def command(self):
        return self.tokens[0]

    @property
    def args(self):
        return self.tokens[1:]
