.. _quickstart:

Quickstart
==========

Eager to get started? This page gives a good introduction in how to get started
with twosheds. This assumes you already have twosheds installed. If you do not,
head over to the :ref:`Installation <install>` section.

Start a Shell
-------------

Interacting with a shell with twosheds is very simple::

    >>> import twosheds
    >>> shell = twosheds.Shell()
    >>> shell.interact()
    $ ls
    AUTHORS.rst       build             requirements.txt  test_twosheds.py
    LICENSE           dist              scripts           tests
    Makefile          docs              setup.cfg         twosheds
    README.rst        env               setup.py          twosheds.egg-info

The Shell is the main interface for twosheds. To quit the shell, just press ``CTRL+D``.

Configuring a shell
-------------------

If we want to configure our shell, it's useful to store our code in a script::

    #!/usr/bin/env python
    import twosheds


    shell = twosheds.Shell()
    shell.interact()

Just copy that into *twosheds* (or whatever you want to call your shell) and
make it executable::

    $ chmod a+x ./twosheds

Then execute it to interact::

    $ ./twosheds
    $ ls
    twosheds

Aliases
-------

To add aliases, we just revise our script to pass in a dictionary full of the
aliases we want to use to the shell::

    #!/usr/bin/env python
    import twosheds


    aliases = {'..': 'cd ..'}

    shell = twosheds.Shell(aliases=aliases)
    shell.interact()

Then we can test it::

    $ ./twosheds
    $ ls
    AUTHORS.rst       build             requirements.txt  test_twosheds.py
    LICENSE           dist              scripts           tests
    Makefile          docs              setup.cfg         twosheds
    README.rst        env               setup.py          twosheds.egg-info
    $ ..
    $ ls
    Desktop/twosheds

Environmental Variables
-----------------------

To set environment variables, just use ``os.environ``::

    PATH = ["/Users/ceasarbautista/local/bin",
            "/Users/ceasarbautista/bin",
            "/usr/local/bin",
            "/usr/bin",
            "/usr/sbin",
            "/bin",
            "/sbin",
            ]

    os.environ['PATH'] = ":".join(PATH)

Make sure to insert code like this before you execute ``interact``.

Change the prompt
-----------------

The prompt for twosheds is just a "$ ". We can change it by subclassing Shell::

    import os

    import twosheds


    class MyShell(twosheds.Shell):
    
        @property
        def prompt(self):
            return os.getcwd() + " "

This is a huge improvement over most ``$PS1`` variables.

The prompt property is read whenever a prompt is written.
