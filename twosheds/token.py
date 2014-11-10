
class LParen(object):
    pass


class RParen(object):
    pass


class Token(object):
    def __init__(self, text):
        self.text = text

    def startswith(self, x):
        return self.text.startswith(x)

    def replace(self, x, y):
        return self.text.replace(x, y)

    def __getitem__(self, x):
        return self.text[x]

    def __str__(self):
        return self.text.replace(" ", "\ ")

    def __repr__(self):
        return str(self)


class Word(Token):
    pass


class DoubleQuote(Token):
    def __str__(self):
        return '"%s"' % self.text
