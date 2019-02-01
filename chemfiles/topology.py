# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from ctypes import c_uint64, c_bool
import numpy as np

from ._utils import CxxPointer
from .atom import Atom
from .residue import Residue


class TopologyAtoms(object):
    """Proxy object to get the atoms in a topology"""

    def __init__(self, topology):
        self.topology = topology

    def __len__(self):
        """Get the current number of atoms in this :py:class:`Topology`."""
        count = c_uint64()
        self.topology.ffi.chfl_topology_atoms_count(self.topology, count)
        return count.value

    def __getitem__(self, index):
        """
        Get a reference to the :py:class:`Atom` at the given ``index`` in the
        associated :py:class:`Topology`.
        """
        if index >= len(self):
            raise IndexError("atom index ({}) out of range for this topology".format(index))
        else:
            ptr = self.topology.ffi.chfl_atom_from_topology(self.topology, c_uint64(index))
            return Atom.from_ptr(ptr)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def __delitem__(self, index):
        self.remove(index)

    def remove(self, index):
        """
        Remove the :py:class:`Atom` atthe given ``index`` from the associated
        :py:class:`Topology`.

        This shifts all the atoms indexes after ``i`` by 1 (n becomes n-1).
        """
        self.topology.ffi.chfl_topology_remove(self.topology, c_uint64(index))

    def append(self, atom):
        """
        Add a copy of the :py:class:`Atom` ``atom`` at the end of this
        :py:class:`Topology`.
        """
        self.topology.ffi.chfl_topology_add_atom(self.topology, atom)


class TopologyResidue(object):
    """Proxy object to get the residues in a topology"""

    def __init__(self, topology):
        self.topology = topology

    def __len__(self):
        """Get the current number of residues in this :py:class:`Topology`."""
        count = c_uint64()
        self.topology.ffi.chfl_topology_residues_count(self.topology, count)
        return count.value

    def __getitem__(self, index):
        """
        Get read-only access to the :py:class:`Residue` at the given ``index``
        from the associated :py:class:`Topology`. The residue index in the
        topology does not necessarily match the residue id.
        """
        if index >= len(self):
            raise IndexError("residue index ({}) out of range for this topology".format(index))
        else:
            ptr = self.topology.ffi.chfl_residue_from_topology(self.topology, c_uint64(index))
            return Residue.from_const_ptr(ptr)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def append(self, residue):
        """
        Add the :py:class:`Residue` ``residue`` to this :py:class:`Topology`.

        The residue ``id`` must not already be in the topology, and the residue
        must contain only atoms that are not already in another residue.
        """
        self.topology.ffi.chfl_topology_add_residue(self.topology, residue)


class Topology(CxxPointer):
    """
    A :py:class:`Topology` contains the definition of all the atoms in the
    system, and the liaisons between the atoms (bonds, angles, dihedrals, ...).
    It will also contain all the residues information if it is available.
    """

    def __init__(self):
        """Create a new empty :py:class:`Topology`."""
        super(Topology, self).__init__(self.ffi.chfl_topology(), is_const=False)

    def __copy__(self):
        return Topology.from_ptr(self.ffi.chfl_topology_copy(self))

    @property
    def atoms(self):
        return TopologyAtoms(self)

    def resize(self, count):
        """
        Resize this :py:class:`Topology` to contain ``count`` atoms. If the
        new number of atoms is bigger than the current number, new atoms will
        be created with an empty name and type. If it is lower than the current
        number of atoms, the last atoms will be removed, together with the
        associated bonds, angles and dihedrals.
        """
        self.ffi.chfl_topology_resize(self, count)

    @property
    def residues(self):
        return TopologyResidue(self)

    def residue_for_atom(self, index):
        """
        Get read-only access to the :py:class:`Residue` containing the atom at
        the given ``index`` from this :py:class:`Topology`; or ``None`` if the
        atom is not part of a residue.
        """
        if index >= len(self.atoms):
            raise IndexError(
                "residue index ({}) out of range for this topology".format(index)
            )
        ptr = self.ffi.chfl_residue_for_atom(self, c_uint64(index))
        if ptr:
            return Residue.from_const_ptr(ptr)
        else:
            return None

    def residues_linked(self, first, second):
        """
        Check if the two :py:class:`Residue` ``first`` and ``second`` from this
        :py:class:`Topology` are linked together, *i.e.* if there is a bond
        between one atom in the first residue and one atom in the second one.
        """
        linked = c_bool()
        self.ffi.chfl_topology_residues_linked(self, first, second, linked)
        return linked.value

    def bonds_count(self):
        """Get the number of bonds in this :py:class:`Topology`."""
        bonds = c_uint64()
        self.ffi.chfl_topology_bonds_count(self, bonds)
        return bonds.value

    def angles_count(self):
        """Get the number of angles in this :py:class:`Topology`."""
        angles = c_uint64()
        self.ffi.chfl_topology_angles_count(self, angles)
        return angles.value

    def dihedrals_count(self):
        """Get the number of dihedral angles in this :py:class:`Topology`."""
        dihedrals = c_uint64()
        self.ffi.chfl_topology_dihedrals_count(self, dihedrals)
        return dihedrals.value

    def impropers_count(self):
        """Get the number of improper angles in this :py:class:`Topology`."""
        impropers = c_uint64()
        self.ffi.chfl_topology_impropers_count(self, impropers)
        return impropers.value

    @property
    def bonds(self):
        """Get the list of bonds in this :py:class:`Topology`."""
        n = self.bonds_count()
        bonds = np.zeros((n, 2), np.uint64)
        self.ffi.chfl_topology_bonds(self, bonds, c_uint64(n))
        return bonds

    @property
    def angles(self):
        """Get the list of angles in this :py:class:`Topology`."""
        n = self.angles_count()
        angles = np.zeros((n, 3), np.uint64)
        self.ffi.chfl_topology_angles(self, angles, c_uint64(n))
        return angles

    @property
    def dihedrals(self):
        """Get the list of dihedral angles in this :py:class:`Topology`."""
        n = self.dihedrals_count()
        dihedrals = np.zeros((n, 4), np.uint64)
        self.ffi.chfl_topology_dihedrals(self, dihedrals, c_uint64(n))
        return dihedrals

    @property
    def impropers(self):
        """Get the list of improper angles in this :py:class:`Topology`."""
        n = self.impropers_count()
        impropers = np.zeros((n, 4), np.uint64)
        self.ffi.chfl_topology_impropers(self, impropers, c_uint64(n))
        return impropers

    def add_bond(self, i, j):
        """
        Add a bond between the atoms at indexes ``i`` and ``j`` in this
        :py:class:`Topology`.
        """
        self.ffi.chfl_topology_add_bond(self, c_uint64(i), c_uint64(j))

    def remove_bond(self, i, j):
        """
        Remove any existing bond between the atoms at indexes ``i`` and ``j``
        in this :py:class:`Topology`.

        This function does nothing if there is no bond between ``i`` and ``j``.
        """
        self.ffi.chfl_topology_remove_bond(self, c_uint64(i), c_uint64(j))
