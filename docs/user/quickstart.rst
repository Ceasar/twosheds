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
    >>> shell.serve_forever()
    $ ls
    AUTHORS.rst       build             requirements.txt  test_twosheds.py
    LICENSE           dist              scripts           tests
    Makefile          docs              setup.cfg         twosheds
    README.rst        env               setup.py          twosheds.egg-info

The Shell is the main interface for twosheds. To quit the shell, just press ``CTRL+D``.

Configuring a shell
-------------------

If we want to configure our shell, it's useful to store our code in a script::

    #!/usr/bin/env python -i
    import twosheds


    shell = twosheds.Shell()
    shell.serve_forever()

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

The default prompt for twosheds is just ``$``. We can change that by setting
``$PS1`` before each interaction::

    import os

    @shell.before_request
    def primary_prompt_string():
        os.environ["PS1"] = os.getcwd().replace(os.environ["HOME"], "~") + " "

This may be more typing then the ``export PS1=\w`` equivalent in `bash`, but
it is easier to follow what is happening, which becomes important as the prompt
becomes more complex.
