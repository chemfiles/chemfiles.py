.. _python-api:

Python interface reference
==========================

The Python interface is built on top of the C interface, using the `ctypes`_
standard module.

.. _ctypes: https://docs.python.org/3/library/ctypes.html

This interface is contained in the :py:mod:`chemfiles` module, and this page list all
the classes and methods in this module.

Error handling
--------------

Chemfiles uses exceptions for error handling, and will only throw one of these
exceptions. The :py:class:`ChemfilesException
<chemfiles.errors.ChemfilesException>` base class can be used to catch all
chemfiles related errors.

.. automodule:: chemfiles.errors
    :members:

Trajectory class
----------------

.. set current module to chemfiles

.. automodule:: chemfiles


.. autoclass:: Trajectory
    :members:

Frame class
-----------

.. autoclass:: Frame
    :members:

UnitCell class
--------------

.. autoclass:: CellShape
    :members:

.. autoclass:: UnitCell
    :members:

Topology class
--------------

.. autoclass:: Topology
    :members:

Atom class
----------

.. autoclass:: Atom
    :members:


Residue class
-------------

.. autoclass:: Residue
    :members:


Selection class
---------------

.. autoclass:: Selection
    :members:
