twosheds
========

.. image:: https://badge.fury.io/py/twosheds.png
    :target: http://badge.fury.io/py/twosheds

.. image:: https://pypip.in/d/twosheds/badge.png
        :target: https://crate.io/packages/twosheds/

twosheds [*]_ is a command language interpreter (shell), written in Python.

Most existing shells are written in C which makes extension difficult. Python
is comparatively easy to learn, read, and write, and is fast enough to operate
as a day-to-day shell::

    >>> import twosheds
    >>> shell = twosheds.Shell()
    >>> shell.interact()
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

Installation
------------

To install twosheds, simply:

.. code-block:: bash

    $ pip install twosheds

You may need to `sudo` if you intend to install system wide.


Documentation
-------------

Documentation is available at http://twosheds.readthedocs.org/en/latest/.


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until its get merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/Ceasar/twosheds
.. _`AUTHORS`: https://github.com/Ceasar/twosheds/blob/master/AUTHORS.rst
.. [*] http://www.youtube.com/watch?v=HLjS3gzHetA
