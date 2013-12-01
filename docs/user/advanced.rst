.. _advanced:

Advanced
========

This section of the docs shows how to do some useful but advanced things
with twosheds.

Change your default shell
-------------------------

If you're serious about the shell you just wrote, you can replace the current
one you're using in no time. Assuming your shell is named ``shell``::

    $ cat /etc/shells >> $HOME/shell
    $ chsh -s $HOME/shell

Before doing so however, you should make a new project on GitHub and add
your code to version control.

Once done, you can use your shell from ``$HOME`` by just symlinking it back::

    $ git clone git@github.com:Ceasar/my_shell.git
    $ ln -s my_shell/shell shell

Note, twosheds is under active development, which means you'll almost
certainly run into a problem from time-to-time. Fortunately, the shell is
designed so that it should be possible to fix and contribute back! :)

Add git branch to prompt
------------------------

Add the current git branch to the prompt::

    class MyShell(twosheds.Shell):

        @property
        def git_branch(self):
            """Get the current git branch or None."""
            try:
                check_output("git symbolic-ref --short HEAD 2> /dev/null",
                             shell=True).strip()
            except CalledProcessError:
                return None

        @property
        def prompt(self):
            pwd = os.getcwd().replace(os.environ["HOME"], "~")
            branch = self.git_branch
            if branch is not None:
                return "%s(%s) " % (pwd, branch)
            else:
                return pwd + " "

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

Automate ``git status``
-----------------------

Automating `git status` is similar to automating `ls`::

    from subprocess import check_output, CalledProcessError

    import twosheds


    class MyShell(twosheds.Shell):

        last_gs = ""

        def read(self):
            try:
                gs = check_output("git status 2> /dev/null", shell=True)
            except CalledProcessError:
                pass
            else:
                if gs != self.last_gs:
                    self.last_gs = gs
                    # show status concisely
                    self.eval("git status -s")
            return super(MyShell, self).read()
