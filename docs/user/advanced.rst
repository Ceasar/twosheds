.. _advanced:

Advanced
========

This section of the docs shows how to do some useful but advanced things
with twosheds.

Automate ``ls``
---------------

We so frequently type ``ls`` that sometimes it seems like it would be nice to
automate it.

In other shells, there are either prebuilt hooks from which we can execute
arbitrary code or we can devise impressive aliases to automatically ls
whenever the state of the directory changes::

    # automate ls in zsh
    # If the contents of the current working directory have changed, `ls`.
    function precmd() {

        a=$(cat ~/.contents)
        b=$(ls)
        if [ $a = $b ]
        then
        else
            emulate -L zsh
                ls
        fi
        ls > ~/.contents
    }

With twosheds it's *much* simpler::

    from subprocess import check_output

    import twosheds


    class MyShell(twosheds.Shell):

        last = ""

        def read(self):
            ls = check_output("ls", shell=True)
            if ls != self.last:
                self.last = ls
                self.eval("ls")
            return super(MyShell, self).read()

This code reads the contents of the current directory before every command
and checks if its different from whatever the contents were before the last
command. If they're different, it runs ``ls``.
