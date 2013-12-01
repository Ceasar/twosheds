.. _api:

Developer Interface
===================

.. module:: twosheds

This part of the documentation covers all the interfaces of twosheds.

Main Interface
--------------

All of twoshed's functionality can be accessed by an instance of the :class:`Shell <Shell>` object.

Lower-Level Classes
~~~~~~~~~~~~~~~~~~~

.. autoclass:: twosheds.cli.CommandLineInterface
   :inherited-members:

.. autoclass:: twosheds.Shell

Command Language
----------------

.. autoclass:: twosheds.language.Language
   :inherited-members:

.. autoclass:: twosheds.grammar.Grammar
   :inherited-members:

.. autoclass:: twosheds.semantics.Semantics
   :inherited-members:

Transformations
~~~~~~~~~~~~~~~

.. autoclass:: twosheds.transformation.AliasTransformation
   :inherited-members:

.. autoclass:: twosheds.transformation.VariableTransformation
   :inherited-members:

.. autoclass:: twosheds.transformation.TildeTransformation
   :inherited-members:

Completion
----------

.. autoclass:: twosheds.completer.Completer
   :inherited-members:
