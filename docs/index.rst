.. psprint documentation master file, created by
   sphinx-quickstart on Fri Jan 15 15:18:08 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to psprint's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Documentation
=============

`Read The Docs <https://psprint.readthedocs.io/en/latest/>`__

.. image:: https://readthedocs.org/projects/psprint/badge/?version=latest
           :target: https://psprint.readthedocs.io/en/latest/?badge=latest
           :alt: Documentation Status


Installation
============

pip
---

Preferred method ``pip install psprint``

`pspman <https://github.com/pradyparanjpe/pspman>`__
----------------------------------------------------

For automated management: updates, etc
``pspman -s -i https://github.com/pradyparanjpe/psprint.git``

Uninstallation
==============

.. _pip-1:

pip
---

``pip uninstall -y psprint``

.. _pspman-1:

pspman
------

Remove installation ``pip uninstall -y psprint``

Remove repository clone ``pspman -s -d psprint``

Configuration
=============

Although prefix can be defined on the fly by passing ``**kwargs``, such
definition may be slow and should be avoided. Frequently used prefixes
should be declared in a configuration file located at standard
locations. Configuration file is in `yaml <https://yaml.org/spec/>`__
format.

Location of configuration files
-------------------------------

Configuration may be specified in any of the following locations:

Root (UNIX ONLY):
~~~~~~~~~~~~~~~~~

This is inhereted by all users of the system

``/etc/psprint/style.yml``

User (HOME):
~~~~~~~~~~~~

**This is discouraged.** Maintaining configuration files in ``$HOME`` is
a bad practice. Such configuration should be in ``$XDG_CONFIG_HOME``.

\`$HOME/.psprintrc\`

User (XDG_CONFIG_HOME):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable is generally set to ``$HOME/.config`` on unix-like
systems. Even if unset, we will still try the ``$HOME/.config``
directory.

``$XFG_CONFIG_HOME/psprint/style.yml``

Local:
~~~~~~

In the current working directory

``.psprintrc``

Configuration format
--------------------

Sections
~~~~~~~~

#. FLAGS

   Following variables may be set as boolean value forms (yes, true,
   false, no).

   -  short: Information prefix is short (1 character).
   -  pad: Information prefix is fixed length, padded with <space>
      wherever necessary.
   -  flush: This is passed to python's print function.

   Following variables may be set to string values

   -  sep: This is passed to python's print function.
   -  end: This is passed to python's print function.
   -  file: *Discouraged* STDOUT gets **appended** to ``file``. This may
      be risky as the file is opened out of context

   .. code:: yaml

      FLAGS:
        # short = False
        pad: True
        flush: True
        # sep =
        # end =

#. ``custom``

   The ``custom`` string is used as prefix index while calling print
   function Following variables may be set as string names or integers
   (ANSI Terminal colors)

   -  pref_color: color of information prefix [black, red, g, 5,
      light blue]
   -  pref_gloss: brightness of information prefix [normal, n,
      1, dim, d, 2, bright, b, 3]
   -  pref_bgcol: background of information prefix <same as
      pref_color>
   -  text_color: color of information text [black, red, g, 5,
      light blue]
   -  text_gloss: brightness of information text [normal, n, 1,
      dim, d, 2, bright, b, 3]
   -  text_bgcol: background of information text <same as
      text_color>

   Following variables may be set as str

   -  pref: <10 character long information prefix string (long form)
   -  pref_s: 1 character information prefix (short form)
      *Remember quotes for special characters*

   .. code:: yaml

      help:
        pref: HELP
        pref_s: "?"
        pref_color: yellow
        pref_bgcol: black
        pref_style: normal
        text_color: white
        text_style: normal
        text_bgcol: black

Usage
=====

Substitute python's print
-------------------------

Import in your script

-  ``from psprint import print``

What does it do
---------------

.. code:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   print()
   print("*** WITHOUT PSPRINT ***")
   print("An output statement which informs the user")
   print("This statement requests the user to act")
   print("A debugging output useless to the user")
   print()

   from psprint import print
   print()
   print("*** WITH PSPRINT ***")
   print("An output statement which informs the user", mark=1)
   print("This statement requests the user to act", mark=2)
   print("A debugging output useless to the user", mark='bug')
   print ()

Screenshot: |image0|

.. |image0| image:: ./output.jpg


psprint
=======

.. automodule:: psprint
   :members:

InfoPrint
=========
.. autoclass:: psprint.printer.InfoPrint
   :members:

Error/Warnings
==============

.. automodule:: psprint.errors
   :members:
