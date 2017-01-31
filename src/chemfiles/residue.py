# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_bool, c_uint64, create_string_buffer

from chemfiles import get_c_library
from chemfiles.errors import _check_handle


class Residue(object):
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
        self.c_lib = get_c_library()
        if resid:
            resid = c_uint64(resid)
        else:
            resid = c_uint64(-1)
        self._handle_ = self.c_lib.chfl_residue(name.encode("utf8"), resid)
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chfl_residue_free(self._handle_)

    def __copy__(self):
        residue = self.__new__(Residue)
        residue.c_lib = get_c_library()
        residue._handle_ = self.c_lib.chfl_residue_copy(self._handle_)
        _check_handle(residue._handle_)
        return residue

    def natoms(self):
        '''Get the current number of atoms in the :py:class:`Residue`.'''
        res = c_uint64()
        self.c_lib.chfl_residue_atoms_count(self._handle_, res)
        return res.value

    def __len__(self):
        '''Get the current number of atoms in the :py:class:`Residue`.'''
        return self.natoms()

    def name(self):
        '''Get the :py:class:`Residue` name'''
        res = create_string_buffer(32)
        self.c_lib.chfl_residue_name(self._handle_, res, 32)
        return res.value.decode("utf8")

    def id(self):
        '''Get the :py:class:`Residue` index in the initial topology'''
        res = c_uint64()
        self.c_lib.chfl_residue_id(self._handle_, res)
        return res.value

    def contains(self, atom):
        '''
        Check if the :py:class:`Residue` contains the atom at index ``atom``.
        '''
        res = c_bool()
        self.c_lib.chfl_residue_contains(self._handle_, c_uint64(atom), res)
        return res.value

    def add_atom(self, atom):
        '''Add the atom index ``atom`` in the :py:class:`Residue`.'''
        self.c_lib.chfl_residue_add_atom(self._handle_, c_uint64(atom))
