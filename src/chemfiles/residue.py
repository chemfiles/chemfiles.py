# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_bool, c_uint64, create_string_buffer
from chemfiles.types import CxxPointer


class Residue(CxxPointer):
    '''
    A :py:class:`Residue` is a group of atoms belonging to the same logical
    unit. They can be small molecules, amino-acids in a protein, monomers in
    polymers, etc.
    '''

    def __init__(self, name, resid=None):
        '''
        Create a new :py:class:`Residue` from a ``name`` and a residue id
        ``resid``.
        '''

        if resid:
            resid = c_uint64(resid)
        else:
            resid = c_uint64(-1)
        ptr = self.ffi.chfl_residue(name.encode("utf8"), resid)
        super(Residue, self).__init__(ptr)

    def __del__(self):
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
        '''Get the current number of atoms in the :py:class:`Residue`.'''
        return self.natoms()

    def name(self):
        '''Get the :py:class:`Residue` name'''
        name = create_string_buffer(32)
        self.ffi.chfl_residue_name(self, name, 32)
        return name.value.decode("utf8")

    def id(self):
        '''Get the :py:class:`Residue` index in the initial topology'''
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
