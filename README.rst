twosheds
========

.. image:: https://badge.fury.io/py/twosheds.png
    :target: http://badge.fury.io/py/twosheds

.. image:: https://pypip.in/d/twosheds/badge.png
        :target: https://crate.io/packages/twosheds/

twosheds is a library, written in Python, for making command language
interpreters, or shells.

Shells like bash are very powerful, but they require you to learn C or clunky
domain-specific scripting languages to extend and customize. twosheds lets you
write your own shell, in Python, which means you can customize it completely:

.. code:: python

    >>> import twosheds
    >>> shell = twosheds.Shell()
    >>> shell.interact()
    $ whoami
    arthurjackson
    $ ls
    AUTHORS.rst       build             requirements.txt  test_twosheds.py
    LICENSE           dist              scripts           tests
    Makefile          docs              setup.cfg         twosheds
    README.rst        env               setup.py          twosheds.egg-info

`Get started now. <quickstart_>`_


Features
--------

- Substitution
- History
- Tab completion
- Highly extensible


Installation
------------

To install twosheds, simply:

.. code-block:: bash

    $ pip install twosheds


Documentation
-------------

Documentation is available at http://twosheds.readthedocs.org/en/latest/.


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until its get merged and published. :) Make sure to add yourself to AUTHORS_.

.. _quickstart: http://twosheds.readthedocs.org/en/latest/user/quickstart.html
.. _`the repository`: http://github.com/Ceasar/twosheds
.. _`AUTHORS`: https://github.com/Ceasar/twosheds/blob/master/AUTHORS.rst
