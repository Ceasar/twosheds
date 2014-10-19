twosheds
========

.. image:: https://badge.fury.io/py/twosheds.png
    :target: http://badge.fury.io/py/twosheds

.. image:: https://pypip.in/d/twosheds/badge.png
        :target: https://crate.io/packages/twosheds/

.. image:: https://travis-ci.org/Ceasar/twosheds.svg?branch=master
    :target: https://travis-ci.org/Ceasar/twosheds

twosheds is a library, written in Python, for making command language
interpreters, or shells.

While shells like bash and zsh are powerful, extending them and customizing them
is hard; you need to write in inexpressive arcane languages, such as bash script
or C. twosheds helps you write and customize your own shell, in pure Python:

.. code:: python

    >>> import twosheds
    >>> shell = twosheds.Shell()
    >>> shell.serve_forever()
    $ whoami
    arthurjackson
    $ ls
    AUTHORS.rst       build             requirements.txt  test_twosheds.py
    LICENSE           dist              scripts           tests
    Makefile          docs              setup.cfg         twosheds
    README.rst        env               setup.py          twosheds.egg-info

`Get started now. <http://twosheds.readthedocs.org/en/latest/user/quickstart.html>`_


Features
--------------------------------------------------------------------------------

- Substitution

- History

- Tab completion

- Highly extensible


Installation
--------------------------------------------------------------------------------

To install twosheds, simply:

.. code-block:: bash

    $ pip install twosheds


Documentation
-------------

Documentation is available at http://twosheds.readthedocs.org/en/latest/.


Contribute
----------

twosheds is under active development and contributions are especially welcome.

#. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.

#. Fork `the repository`_ on GitHub to start making your changes to the
   **master** branch (or branch off it).

#. Write a test which shows that the bug was fixed or that the feature works as
   expected.

#. Send a pull request and bug the maintainer until its get merged and
   published. Make sure to add yourself to AUTHORS_. :)


Support
--------------------------------------------------------------------------------

If you have questions or issues about twosheds, there are several options:

Send a Tweet
~~~~~~~~~~~~

If your question is less than 140 characters, feel free to tweet at the
maintainer, `@Ceasar_Bautista`_.

File an Issue
~~~~~~~~~~~~~

If you notice some unexpected behavior in twosheds, or want to see support for
a new feature, `file an issue on GitHub issues`_.

E-mail
~~~~~~

I'm more than happy to answer any personal or in-depth questions about twosheds.
Feel free to email `cbautista@gmail.com`_.


.. _`the repository`: http://github.com/Ceasar/twosheds
.. _`AUTHORS`: https://github.com/Ceasar/twosheds/blob/master/AUTHORS.rst
.. _@Ceasar_Bautista: https://twitter.com/Ceasar_Bautista
.. _file an issue on Github issues: https://github.com/Ceasar/twosheds/issues
.. _cbautista@gmail.com: mailto:cbautista@gmail.com
