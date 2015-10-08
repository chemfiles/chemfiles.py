# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_size_t, c_bool, byref, POINTER
import numpy as np

from .ffi import get_c_library
from .errors import _check_handle, ChemfilesException
from .atom import Atom


class Topology(object):
    '''
    A `Topology` contains the definition of all the particles in the system,
    and the liaisons between the particles (bonds, angles, dihedrals, ...).

    Only the atoms and the bonds are stored, the angles and the dihedrals are
    computed automaticaly.
    '''

    def __init__(self):
        '''Create a new empty ``Topology``.'''
        self.c_lib = get_c_library()
        self._handle_ = self.c_lib.chfl_topology()
        _check_handle(self._handle_)

    def __del__(self):
        self.c_lib.chfl_topology_free(self._handle_)

    def atom(self, index):
        '''Get the ``Atom`` at ``index`` from a topology.'''
        atom = Atom("")
        self.c_lib.chfl_atom_free(atom._handle_)
        atom._handle_ = self.c_lib.chfl_atom_from_topology(
            self._handle_, c_size_t(index)
        )
        try:
            _check_handle(atom._handle_)
        except ChemfilesException:
            raise IndexError("Not atom at index {} in frame".format(index))
        return atom

    def natoms(self):
        '''Get the current number of atoms in the ``Topology``.'''
        res = c_size_t()
        self.c_lib.chfl_topology_atoms_count(self._handle_, res)
        return res.value

    def __len__(self):
        '''Get the current number of atoms in the ``Topology``.'''
        return self.natoms()

    def append(self, atom):
        '''Add an ``Atom`` at the end of the ``Topology``'''
        self.c_lib.chfl_topology_append(self._handle_, atom._handle_)

    def remove(self, index):
        '''
        Remove an ``Atom`` from the ``Topology`` by index. This modify all the
        other atoms indexes.
        '''
        self.c_lib.chfl_topology_remove(self._handle_, c_size_t(index))

    def isbond(self, i, j):
        '''Tell if the atoms at indexes ``i`` and ``j`` are bonded together'''
        res = c_bool()
        self.c_lib.chfl_topology_isbond(
            self._handle_, c_size_t(i), c_size_t(j), byref(res)
        )
        return res.value

    def isangle(self, i, j, k):
        '''
        Tell if the atoms at indexes ``i``, ``j`` and ``k`` constitues an angle
        '''
        res = c_bool()
        self.c_lib.chfl_topology_isangle(
            self._handle_, c_size_t(i), c_size_t(j), c_size_t(k), byref(res)
        )
        return res.value

    def isdihedral(self, i, j, k, m):
        '''
        Tell if the atoms at indexes ``i``, ``j``, ``k`` and ``m`` constitues a
        dihedral angle
        '''
        res = c_bool()
        self.c_lib.chfl_topology_isdihedral(
            self._handle_,
            c_size_t(i), c_size_t(j), c_size_t(k), c_size_t(m),
            byref(res)
        )
        return res.value

    def bonds_count(self):
        '''Get the number of bonds in the system'''
        res = c_size_t()
        self.c_lib.chfl_topology_bonds_count(self._handle_, byref(res))
        return res.value

    def angles_count(self):
        '''Get the number of angles in the system'''
        res = c_size_t()
        self.c_lib.chfl_topology_angles_count(self._handle_, byref(res))
        return res.value

    def dihedrals_count(self):
        '''Get the number of dihedral angles in the system'''
        res = c_size_t()
        self.c_lib.chfl_topology_dihedrals_count(self._handle_, byref(res))
        return res.value

    def bonds(self):
        '''Get the list of bonds in the system'''
        nbonds = self.bonds_count()
        res = np.zeros((nbonds, 2), np.uintp)
        self.c_lib.chfl_topology_bonds(self._handle_, res, c_size_t(nbonds))
        return res

    def angles(self):
        '''Get the list of angles in the system'''
        nangles = self.angles_count()
        res = np.zeros((nangles, 3), np.uintp)
        self.c_lib.chfl_topology_angles(self._handle_, res, c_size_t(nangles))
        return res

    def dihedrals(self):
        '''Get the list of dihedral angles in the system'''
        ndihedrals = self.dihedrals_count()
        res = np.zeros((ndihedrals, 4), np.uintp)
        self.c_lib.chfl_topology_dihedrals(self._handle_, res, c_size_t(ndihedrals))
        return res

    def add_bond(self, i, j):
        '''
        Add a bond between the atoms at indexes ``i`` and ``j`` in the system
        '''
        self.c_lib.chfl_topology_add_bond(self._handle_, c_size_t(i), c_size_t(j))

    def remove_bond(self, i, j):
        '''
        Remove any existing bond between the atoms at indexes ``i`` and ``j``
        in the system
        '''
        self.c_lib.chfl_topology_remove_bond(
            self._handle_, c_size_t(i), c_size_t(j)
        )
