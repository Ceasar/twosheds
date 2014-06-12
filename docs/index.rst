.. twosheds documentation master file, created by
   sphinx-quickstart on Sat Nov 30 21:42:38 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

twosheds
========

Release v\ |version|. (:ref:`Installation <install>`)

twosheds is a library for making command language interpreters, or shells.

While shells like bash and zsh are powerful, extending them and customizing them
is hard; you need to write in arcane inexpressive languages, such as bash script
or C. twosheds helps you write and customize your own shell, in pure Python:

.. code:: python

    >>> import twosheds
    >>> shell = twosheds.Shell()
    >>> shell.serve_forever()
    $ ls
    AUTHORS.rst       build             requirements.txt  test_twosheds.py
    LICENSE           dist              scripts           tests
    Makefile          docs              setup.cfg         twosheds
    README.rst        env               setup.py          twosheds.egg-info

Features
--------

- Highly extensible
- History
- Completion

User Guide
----------

This part of the documentation focuses on step-by-step instructions for getting
the most of twosheds.

.. toctree::
   :maxdepth: 2

   user/install
   user/quickstart
   user/advanced

Community Guide
-----------------

This part of the documentation, which is mostly prose, details the
Requests ecosystem and community.

.. toctree::
   :maxdepth: 1

   community/support
   community/updates

API Documentation
-----------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Contributor Guide
-----------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 1

   dev/todo
   dev/authors
