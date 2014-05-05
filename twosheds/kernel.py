import subprocess


class Kernel(object):
    def respond(self, text):
        process = subprocess.Popen(text, shell=True)
        process.communicate()
