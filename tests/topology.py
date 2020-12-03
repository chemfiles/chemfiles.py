# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy
import numpy as np

from chemfiles import Topology, Atom, Residue, BondOrder, ChemfilesError
from _utils import remove_warnings


class TestTopology(unittest.TestCase):
    def test_repr(self):
        topology = Topology()
        self.assertEqual(topology.__repr__(), "Topology with 0 atoms")
        topology.resize(4)
        self.assertEqual(topology.__repr__(), "Topology with 4 atoms")

        self.assertEqual(
            topology.atoms.__repr__(), "[Atom(''), Atom(''), Atom(''), Atom('')]"
        )

        topology.residues.append(Residue("ALA"))
        topology.residues.append(Residue("ARG"))
        self.assertEqual(
            topology.residues.__repr__(),
            "[Residue('ALA') with 0 atoms, Residue('ARG') with 0 atoms]",
        )

    def test_copy(self):
        topology = Topology()
        topology.resize(4)
        cloned = copy.copy(topology)

        self.assertEqual(len(topology.atoms), 4)
        self.assertEqual(len(cloned.atoms), 4)

        topology.resize(8)
        self.assertEqual(len(topology.atoms), 8)
        self.assertEqual(len(cloned.atoms), 4)

    def test_size(self):
        topology = Topology()

        self.assertEqual(len(topology.atoms), 0)

        topology.atoms.append(Atom("H"))
        topology.atoms.append(Atom("O"))
        topology.atoms.append(Atom("O"))
        topology.atoms.append(Atom("H"))

        self.assertEqual(len(topology.atoms), 4)
        topology.resize(8)
        self.assertEqual(len(topology.atoms), 8)

        topology.atoms.remove(3)
        self.assertEqual(len(topology.atoms), 7)

        del topology.atoms[4]
        self.assertEqual(len(topology.atoms), 6)

    def test_bonds(self):
        topology = Topology()
        topology.resize(4)
        self.assertEqual(topology.bonds_count(), 0)

        topology.add_bond(0, 1)
        topology.add_bond(1, 2)
        topology.add_bond(2, 3)

        self.assertEqual(topology.bonds_count(), 3)
        self.assertEqual(topology.bonds.all(), np.array([[2, 3], [1, 2], [0, 1]]).all())

        topology.remove_bond(2, 3)
        self.assertEqual(topology.bonds_count(), 2)

        self.assertEqual(topology.bonds_order(0, 1), BondOrder.Unknown)
        self.assertEqual(topology.bonds_order(1, 2), BondOrder.Unknown)

        with remove_warnings:
            with self.assertRaises(ChemfilesError):
                _ = topology.bonds_order(1, 3)

        topology.add_bond(2, 3, BondOrder.Aromatic)
        self.assertEqual(topology.bonds_order(2, 3), BondOrder.Aromatic)
        self.assertEqual(
            topology.bonds_orders,
            [BondOrder.Unknown, BondOrder.Unknown, BondOrder.Aromatic],
        )

        topology.clear_bonds()
        self.assertEqual(topology.bonds_count(), 0)

    def test_angles(self):
        topology = Topology()
        topology.resize(4)
        self.assertEqual(topology.angles_count(), 0)

        topology.add_bond(0, 1)
        topology.add_bond(1, 2)
        topology.add_bond(2, 3)

        self.assertEqual(topology.angles_count(), 2)
        self.assertEqual(topology.angles.all(), np.array([[0, 1, 2], [1, 2, 3]]).all())

    def test_dihedrals(self):
        topology = Topology()
        topology.resize(4)
        self.assertEqual(topology.dihedrals_count(), 0)

        topology.add_bond(0, 1)
        topology.add_bond(1, 2)
        topology.add_bond(2, 3)

        self.assertEqual(topology.dihedrals_count(), 1)
        self.assertEqual(topology.dihedrals.all(), np.array([[0, 1, 2, 3]]).all())

    def test_impropers(self):
        topology = Topology()
        topology.resize(4)
        self.assertEqual(topology.impropers_count(), 0)

        topology.add_bond(1, 0)
        topology.add_bond(1, 2)
        topology.add_bond(1, 3)

        self.assertEqual(topology.impropers_count(), 1)
        self.assertEqual(topology.impropers.all(), np.array([[0, 1, 2, 3]]).all())

    def test_out_of_bounds(self):
        topology = Topology()
        topology.resize(4)

        residue = Residue("")
        residue.atoms.append(1)
        topology.residues.append(residue)

        _ = topology.atoms[2]
        _ = topology.residues[0]
        _ = topology.residue_for_atom(1)

        with self.assertRaises(IndexError):
            _ = topology.atoms[6]

        with self.assertRaises(IndexError):
            _ = topology.residues[6]

        with self.assertRaises(IndexError):
            _ = topology.residue_for_atom(6)

    def test_residues(self):
        topology = Topology()
        topology.resize(6)

        residue = Residue("foo", 4)
        residue.atoms.append(3)
        residue.atoms.append(4)
        topology.residues.append(residue)

        residue = Residue("bar", 67)
        residue.atoms.append(1)
        residue.atoms.append(2)
        topology.residues.append(residue)

        self.assertEqual(topology.residue_for_atom(5), None)

        first = topology.residues[0]
        self.assertEqual(first.name, "foo")

        second = topology.residues[1]
        self.assertEqual(second.name, "bar")

        self.assertFalse(topology.residues_linked(first, second))

        topology.add_bond(2, 3)
        self.assertTrue(topology.residues_linked(first, second))

    def test_iter(self):
        topology = Topology()
        topology.resize(6)

        for i, atom in enumerate(topology.atoms):
            self.assertEqual(atom.name, "")
        self.assertEqual(i, 5)

        topology.residues.append(Residue("foo"))
        topology.residues.append(Residue("foo"))
        topology.residues.append(Residue("foo"))

        for i, residue in enumerate(topology.residues):
            self.assertEqual(residue.name, "foo")
        self.assertEqual(i, 2)


if __name__ == "__main__":
    unittest.main()
