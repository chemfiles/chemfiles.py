# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy
import numpy as np

from chemfiles import Topology, Atom, Residue


class TestTopology(unittest.TestCase):
    def test_copy(self):
        topology = Topology()
        topology.resize(4)
        cloned = copy.copy(topology)

        self.assertEqual(topology.natoms(), 4)
        self.assertEqual(cloned.natoms(), 4)

        topology.resize(8)
        self.assertEqual(topology.natoms(), 8)
        self.assertEqual(cloned.natoms(), 4)

    def test_size(self):
        topology = Topology()

        self.assertEqual(topology.natoms(), 0)
        self.assertEqual(len(topology), 0)

        topology.add_atom(Atom("H"))
        topology.add_atom(Atom("O"))
        topology.add_atom(Atom("O"))
        topology.add_atom(Atom("H"))

        self.assertEqual(len(topology), 4)
        topology.resize(8)
        self.assertEqual(len(topology), 8)

        topology.remove(3)
        self.assertEqual(len(topology), 7)

    def test_bonding(self):
        topology = Topology()
        topology.resize(4)
        self.assertEqual(topology.bonds_count(), 0)
        self.assertEqual(topology.angles_count(), 0)
        self.assertEqual(topology.dihedrals_count(), 0)

        topology.add_bond(0, 1)
        topology.add_bond(1, 2)
        topology.add_bond(2, 3)

        self.assertEqual(topology.bonds_count(), 3)
        self.assertEqual(topology.angles_count(), 2)
        self.assertEqual(topology.dihedrals_count(), 1)

        self.assertEqual(
            topology.bonds().all(),
            np.array([[2, 3], [1, 2], [0, 1]]).all()
        )

        self.assertEqual(
            topology.angles().all(),
            np.array([[0, 1, 2], [1, 2, 3]]).all()
        )

        self.assertEqual(
            topology.dihedrals().all(),
            np.array([[0, 1, 2, 3]]).all()
        )

        topology.remove_bond(2, 3)
        self.assertEqual(topology.bonds_count(), 2)
        self.assertEqual(topology.angles_count(), 1)
        self.assertEqual(topology.dihedrals_count(), 0)

    def test_out_of_bounds(self):
        topology = Topology()
        topology.resize(4)

        residue = Residue("")
        residue.add_atom(1)
        topology.add_residue(residue)

        topology.atom(2)
        topology.residue(0)
        topology.residue_for_atom(1)

        self.assertRaises(IndexError, topology.atom, 6)
        self.assertRaises(IndexError, topology.residue, 6)
        self.assertRaises(IndexError, topology.residue_for_atom, 6)

    def test_residues(self):
        topology = Topology()
        topology.resize(6)

        residue = Residue('foo', 4)
        residue.add_atom(3)
        residue.add_atom(4)
        topology.add_residue(residue)

        residue = Residue('bar', 67)
        residue.add_atom(1)
        residue.add_atom(2)
        topology.add_residue(residue)

        self.assertEqual(topology.residue_for_atom(5), None)

        first = topology.residue(0)
        self.assertEqual(first.name(), 'foo')

        second = topology.residue(1)
        self.assertEqual(second.name(), 'bar')

        self.assertFalse(topology.residues_linked(first, second))

        topology.add_bond(2, 3)
        self.assertTrue(topology.residues_linked(first, second))

    def test_iter(self):
        topology = Topology()
        topology.resize(6)

        i = 0
        for atom in topology:
            self.assertEqual(atom.name(), "")
            i += 1
        self.assertEqual(i, 6)


if __name__ == '__main__':
    unittest.main()
