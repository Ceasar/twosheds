.. _advanced:

Advanced
========

This section of the docs shows you how to do useful but advanced things with
twosheds.

Change your login shell
-----------------------

Replacing your login shell the shell you just wrote is simple.

Let's assume your shell is named ``$SHELLPATH``. First you need to add your
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

    $ sudo bash -c "echo $SHELLPATH >> /etc/shells"

Finally, change your login shell::

    $ chsh -s $SHELLPATH

Add git branch to prompt
------------------------

Add the current git branch to the prompt::

    def git_branch():
        """Get the current git branch or None."""
        try:
            return check_output("git symbolic-ref --short HEAD 2> /dev/null",
                                shell=True).strip()
        except CalledProcessError:
            return None

    @shell.before_request
    def primary_prompt_string():
        pwd = os.getcwd().replace(os.environ["HOME"], "~")
        branch = git_branch()
        ps1 = "%s " % pwd if branch is None else "%s(%s) " % (pwd, branch)
        os.environ["PS1"] = ps1

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


    shell = twosheds.Shell()
    last_ls = ""


    @shell.before_request
    def ls():
        global last_ls
        ls = check_output("ls", shell=True)
        if ls != last_ls:
            last_ls = ls
            shell.eval("ls")

This code reads the contents of the current directory before every command
and checks if its different from whatever the contents were before the last
command. If they're different, it runs ``ls``.

Automate ``git status``
-----------------------

Automating `git status` is similar to automating `ls`::

    from subprocess import check_output, CalledProcessError

    import twosheds


    shell = twosheds.Shell()
    last_gs = ""


    @shell.before_request
    def gs():
        global last_gs
        try:
            gs = check_output("git status --porcelain 2> /dev/null", shell=True)
        except CalledProcessError:
            pass
        else:
            if gs != last_gs:
                last_gs = gs
                # show status concisely
                shell.eval("git status -s")
