# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_bool, c_uint64
import numpy as np

from ._utils import CxxPointer, _call_with_growing_buffer


class ResidueAtoms(object):
    """Proxy object to get the atomic indexes in a residue"""

    def __init__(self, residue):
        self.residue = residue
        # Use a cache for indexes
        self.indexes = None

    def __len__(self):
        """Get the current number of atoms in this :py:class:`Residue`."""
        if self.indexes is not None:
            return len(indexes)
        else:
            count = c_uint64()
            self.residue.ffi.chfl_residue_atoms_count(self.residue, count)
            return count.value

    def __contains__(self, index):
        """
        Check if the :py:class:`Residue` contains the atom at index ``atom``.
        """
        if self.indexes is not None:
            return index in self.indexes
        else:
            result = c_bool()
            self.residue.ffi.chfl_residue_contains(self.residue, c_uint64(index), result)
            return result.value

    def __getitem__(self, i):
        """
        Get the atomic index number ``i`` in the associated :py:class:`Residue`.
        """
        if self.indexes is None:
            count = len(self)
            self.indexes = np.zeros(count, np.uint64)
            self.residue.ffi.chfl_residue_atoms(self.residue, self.indexes, c_uint64(count))

        return self.indexes[i]

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def append(self, atom):
        """Add the atom index ``atom`` in the :py:class:`Residue`."""
        self.residue.ffi.chfl_residue_add_atom(self.residue, c_uint64(atom))
        # reset the cache for indexes
        self.indexes = None


class Residue(CxxPointer):
    """
    A :py:class:`Residue` is a group of atoms belonging to the same logical
    unit. They can be small molecules, amino-acids in a protein, monomers in
    polymers, etc.
    """

    def __init__(self, name, resid=None):
        """
        Create a new :py:class:`Residue` from a ``name`` and optionally a
        residue id ``resid``.
        """

        if resid:
            ptr = self.ffi.chfl_residue_with_id(name.encode("utf8"), c_uint64(resid))
        else:
            ptr = self.ffi.chfl_residue(name.encode("utf8"))
        super(Residue, self).__init__(ptr, is_const=False)

    def __copy__(self):
        return Residue.from_ptr(self.ffi.chfl_residue_copy(self))

    @property
    def name(self):
        """Get the name of this :py:class:`Residue`."""
        return _call_with_growing_buffer(
            lambda buff, size: self.ffi.chfl_residue_name(self, buff, size), initial=32
        )

    @property
    def id(self):
        """Get the :py:class:`Residue` index in the initial topology."""
        id = c_uint64()
        self.ffi.chfl_residue_id(self, id)
        return id.value

    @property
    def atoms(self):
        return ResidueAtoms(self)
