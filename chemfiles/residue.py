# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_bool, c_uint64
import numpy as np

from .utils import CxxPointer, _call_with_growing_buffer


class Residue(CxxPointer):
    '''
    A :py:class:`Residue` is a group of atoms belonging to the same logical
    unit. They can be small molecules, amino-acids in a protein, monomers in
    polymers, etc.
    '''

    def __init__(self, name, resid=None):
        '''
        Create a new :py:class:`Residue` from a ``name`` and optionally a
        residue id ``resid``.
        '''

        if resid:
            ptr = self.ffi.chfl_residue_with_id(
                name.encode("utf8"), c_uint64(resid)
            )
        else:
            ptr = self.ffi.chfl_residue(name.encode("utf8"))
        super(Residue, self).__init__(ptr)

    def __del__(self):
        if hasattr(self, 'ptr'):
            self.ffi.chfl_residue_free(self)

    def __copy__(self):
        residue = self.__new__(Residue)
        super(Residue, residue).__init__(self.ffi.chfl_residue_copy(self))
        return residue

    def natoms(self):
        '''Get the current number of atoms in the :py:class:`Residue`.'''
        natoms = c_uint64()
        self.ffi.chfl_residue_atoms_count(self, natoms)
        return natoms.value

    def __len__(self):
        '''Get the current number of atoms in this :py:class:`Residue`.'''
        return self.natoms()

    def name(self):
        '''Get the name of this :py:class:`Residue`.'''
        return _call_with_growing_buffer(
            lambda buff, size: self.ffi.chfl_residue_name(self, buff, size),
            initial=32,
        )

    def id(self):
        '''Get the :py:class:`Residue` index in the initial topology.'''
        id = c_uint64()
        self.ffi.chfl_residue_id(self, id)
        return id.value

    def contains(self, atom):
        '''
        Check if the :py:class:`Residue` contains the atom at index ``atom``.
        '''
        contained = c_bool()
        self.ffi.chfl_residue_contains(self, c_uint64(atom), contained)
        return contained.value

    def add_atom(self, atom):
        '''Add the atom index ``atom`` in the :py:class:`Residue`.'''
        self.ffi.chfl_residue_add_atom(self, c_uint64(atom))

    def atoms(self):
        '''Get the indexes of the atoms in this :py:class:`Residue`.'''
        n = len(self)
        atoms = np.zeros(n, np.uint64)
        self.ffi.chfl_residue_atoms(self, atoms, c_uint64(n))
        return atoms
