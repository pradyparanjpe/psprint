#####
USAGE
#####

Substitute python's print
=========================

Import in your script.

.. code:: python

          from psprint import print

Supply value for ``mark`` kwarg or for any of the custom kwargs as described.

.. code:: python

          print("", mark="info")


.. note::

    You may have to add exception to ``${XDG_CONFIG_HOME}/pylintrc`` if you use linter

.. code:: ini

    [VARIABLES]
    redefining-builtins-modules=psprint


Configure frequently used ``mark`` in a suitably `located <configure.html#location-of-configuration-files>`__ configuration file.


Substitute use as pretty repr
=============================

Import in your script.

.. code:: python

          from psprint import psfmt

Supply value for ``mark`` kwarg or for any of the custom kwargs as described.

.. code:: python

          class MyFmtClass():
              """My Test Class with format string"""
              def __init__(self):
                  self.attr = 'data'

              def __repr__(self) -> str:
                  return 'data: {self.attr!s}'

              def __format__(self, spec):
                  fmt_out = []
                  for line_no, line in enumerate(self.__repr__().split("\n")):
                      if line_no == 0:
                          fmt_out.extend(psfmt(line, mark=spec))
                      else:
                          fmt_out.extend(psfmt(line, mark='cont'))
                  return '\n'.join(fmt_out)


.. warning::

   Do not use this as a substitite for ``repr(object)``.
   This function only returns a ps-representation of supplied string.

.. code:: ini

    [VARIABLES]
    redefining-builtins-modules=psfmt


Configure frequently used ``mark`` in a suitably `located <configure.html#location-of-configuration-files>`__ configuration file.
