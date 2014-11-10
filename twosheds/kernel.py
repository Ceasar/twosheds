import pexpect


class Kernel(object):
    def __init__(self):
        self.child = pexpect.spawn('bash -i')

    def respond(self, text):
        self.child.sendline(text)
        self.child.expect('%s(.*)bash-3.2\$ ' % text)
        match = self.child.match.group(0)
        return match
