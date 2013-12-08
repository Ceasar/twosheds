

class Lexicon(object):
    def lex(self, text):
        return text.replace(";", " ; ").split(" ")
