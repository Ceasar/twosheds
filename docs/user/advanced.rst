.. _advanced:

Advanced
========

This section of the docs shows you how to do useful but advanced things with
twosheds.

Change your login shell
-----------------------

Replacing your login shell the shell you just wrote is simple.

Let's assume your shell is named ``$HOME/shell``. First you need to add your
shell to the list of valid shells, and then you need to actually change it.

To add your shell to the list of valid shells, you need to add it to
``/etc/shells``, a list of paths to valid login shells on the system. By
default, it looks something like this::

    # List of acceptable shells for chpass(1).
    # Ftpd will not allow users to connect who are not using
    # one of these shells.

    /bin/bash
    /bin/csh
    /bin/ksh
    /bin/sh
    /bin/tcsh
    /bin/zsh

So to add your shell, simply::

    $ sudo cat $HOME/shell >> /etc/shells

Finally, change your login shell::

    $ chsh -s $HOME/shell

Add git branch to prompt
------------------------

Add the current git branch to the prompt::

    class MyShell(twosheds.Shell):

        @property
        def git_branch(self):
            """Get the current git branch or None."""
            try:
                return check_output("git symbolic-ref --short HEAD 2> /dev/null",
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

        @property
        def git_status(self):
            try:
                return check_output("git status --porcelain 2> /dev/null", shell=True)
            except CalledProcessError:
                return None

        def read(self):
            gs = self.git_status
            if gs is not None and gs != self.last_gs:
                self.last_gs = gs
                # show status concisely
                self.eval("git status -s")
            return super(MyShell, self).read()
