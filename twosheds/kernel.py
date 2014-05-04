import subprocess


class Kernel(object):
    def respond(self, request):
        process = subprocess.Popen(request.text, shell=True)
        process.communicate()
