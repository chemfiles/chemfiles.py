# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_uint64, c_bool
import numpy as np

from .utils import CxxPointer
from .atom import Atom
from .residue import Residue


class Topology(CxxPointer):
    '''
    A :py:class:`Topology` contains the definition of all the atoms in the
    system, and the liaisons between the atoms (bonds, angles, dihedrals, ...).
    It will also contain all the residues information if it is available.
    '''

    def __init__(self):
        '''Create a new empty :py:class:`Topology`.'''
        super(Topology, self).__init__(self.ffi.chfl_topology())

    def __del__(self):
        if hasattr(self, 'ptr'):
            self.ffi.chfl_topology_free(self)

    def __copy__(self):
        return Topology.from_ptr(self.ffi.chfl_topology_copy(self))

    def __iter__(self):
        for i in range(self.natoms()):
            yield self.atom(i)

    def atom(self, i):
        '''
        Get a copy of the :py:class:`Atom` at index ``i`` from this
        :py:class:`Topology`.
        '''
        if i >= self.natoms():
            raise IndexError(
                "atom index ({}) out of range for this topology".format(i)
            )
        return Atom.from_ptr(
            self.ffi.chfl_atom_from_topology(self, c_uint64(i))
        )

    def natoms(self):
        '''Get the number of atoms in this :py:class:`Topology`.'''
        natoms = c_uint64()
        self.ffi.chfl_topology_atoms_count(self, natoms)
        return natoms.value

    def __len__(self):
        '''Get the number of atoms in this :py:class:`Topology`.'''
        return self.natoms()

    def resize(self, natoms):
        '''
        Resize this :py:class:`Topology` to contain ``natoms`` atoms. If the
        new number of atoms is bigger than the current number, new atoms will
        be created with an empty name and type. If it is lower than the current
        number of atoms, the last atoms will be removed, together with the
        associated bonds, angles and dihedrals.
        '''
        self.ffi.chfl_topology_resize(self, natoms)

    def add_atom(self, atom):
        '''
        Add a copy of the :py:class:`Atom` ``atom`` at the end of this
        :py:class:`Topology`.
        '''
        self.ffi.chfl_topology_add_atom(self, atom)

    def remove(self, i):
        '''
        Remove the :py:class:`Atom` at index `i` from this
        :py:class:`Topology`.

        This shifts all the atoms indexes after ``i`` by 1 (n becomes n-1).
        '''
        self.ffi.chfl_topology_remove(self, c_uint64(i))

    def residue(self, i):
        '''
        Get the :py:class:`Residue` at index ``i`` from this
        :py:class:`Topology`.
        '''
        if i >= self.residues_count():
            raise IndexError(
                "residue index ({}) out of range for this topology".format(i)
            )
        return Residue.from_ptr(
            self.ffi.chfl_residue_from_topology(self, c_uint64(i))
        )

    def residue_for_atom(self, i):
        '''
        Get the :py:class:`Residue` containing the atom at index ``i`` from
        this :py:class:`Topology`. If the atom is not in a residue, this
        function returns None.
        '''
        if i >= self.natoms():
            raise IndexError(
                "residue index ({}) out of range for this topology".format(i)
            )
        ptr = self.ffi.chfl_residue_for_atom(self, c_uint64(i))
        if ptr:
            return Residue.from_ptr(ptr)
        else:
            return None

    def residues_count(self):
        '''Get the number of residues in this :py:class:`Topology`.'''
        residues = c_uint64()
        self.ffi.chfl_topology_residues_count(self, residues)
        return residues.value

    def add_residue(self, residue):
        '''
        Add the :py:class:`Residue` ``residue`` to this :py:class:`Topology`.

        The residue ``id`` must not already be in the topology, and the residue
        must contain only atoms that are not already in another residue.
        '''
        self.ffi.chfl_topology_add_residue(self, residue)

    def residues_linked(self, first, second):
        '''
        Check if the two :py:class:`Residue` ``first`` and ``second`` from this
        :py:class:`Topology` are linked together, *i.e.* if there is a bond
        between one atom in the first residue and one atom in the second one.
        '''
        linked = c_bool()
        self.ffi.chfl_topology_residues_linked(self, first, second, linked)
        return linked.value

    def bonds_count(self):
        '''Get the number of bonds in this :py:class:`Topology`.'''
        bonds = c_uint64()
        self.ffi.chfl_topology_bonds_count(self, bonds)
        return bonds.value

    def angles_count(self):
        '''Get the number of angles in this :py:class:`Topology`.'''
        angles = c_uint64()
        self.ffi.chfl_topology_angles_count(self, angles)
        return angles.value

    def dihedrals_count(self):
        '''Get the number of dihedral angles in this :py:class:`Topology`.'''
        dihedrals = c_uint64()
        self.ffi.chfl_topology_dihedrals_count(self, dihedrals)
        return dihedrals.value

    def impropers_count(self):
        '''Get the number of improper angles in this :py:class:`Topology`.'''
        impropers = c_uint64()
        self.ffi.chfl_topology_impropers_count(self, impropers)
        return impropers.value

    def bonds(self):
        '''Get the list of bonds in this :py:class:`Topology`.'''
        n = self.bonds_count()
        bonds = np.zeros((n, 2), np.uint64)
        self.ffi.chfl_topology_bonds(self, bonds, c_uint64(n))
        return bonds

    def angles(self):
        '''Get the list of angles in this :py:class:`Topology`.'''
        n = self.angles_count()
        angles = np.zeros((n, 3), np.uint64)
        self.ffi.chfl_topology_angles(self, angles, c_uint64(n))
        return angles

    def dihedrals(self):
        '''Get the list of dihedral angles in this :py:class:`Topology`.'''
        n = self.dihedrals_count()
        dihedrals = np.zeros((n, 4), np.uint64)
        self.ffi.chfl_topology_dihedrals(self, dihedrals, c_uint64(n))
        return dihedrals

    def impropers(self):
        '''Get the list of improper angles in this :py:class:`Topology`.'''
        n = self.impropers_count()
        impropers = np.zeros((n, 4), np.uint64)
        self.ffi.chfl_topology_impropers(self, impropers, c_uint64(n))
        return impropers

    def add_bond(self, i, j):
        '''
        Add a bond between the atoms at indexes ``i`` and ``j`` in this
        :py:class:`Topology`.
        '''
        self.ffi.chfl_topology_add_bond(self, c_uint64(i), c_uint64(j))

    def remove_bond(self, i, j):
        '''
        Remove any existing bond between the atoms at indexes ``i`` and ``j``
        in this :py:class:`Topology`.

        This function does nothing if there is no bond between ``i`` and ``j``.
        '''
        self.ffi.chfl_topology_remove_bond(self, c_uint64(i), c_uint64(j))
