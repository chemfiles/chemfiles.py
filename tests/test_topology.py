# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import numpy as np

from chemfiles import Topology, Atom


class TestTopology(unittest.TestCase):
    def test_topology(self):
        topology = Topology()

        self.assertEqual(topology.natoms(), 0)
        self.assertEqual(len(topology), 0)

        H = Atom("H")
        O = Atom("O")

        topology.append(H)
        topology.append(O)
        topology.append(O)
        topology.append(H)

        self.assertEqual(len(topology), 4)
        self.assertEqual(topology.bonds_count(), 0)
        self.assertEqual(topology.angles_count(), 0)
        self.assertEqual(topology.dihedrals_count(), 0)

        topology.add_bond(0, 1)
        topology.add_bond(1, 2)
        topology.add_bond(2, 3)

        self.assertEqual(topology.bonds_count(), 3)
        self.assertEqual(topology.angles_count(), 2)
        self.assertEqual(topology.dihedrals_count(), 1)

        self.assertTrue(topology.isbond(0, 1))
        self.assertFalse(topology.isbond(0, 3))

        self.assertTrue(topology.isangle(0, 1, 2))
        self.assertFalse(topology.isangle(0, 1, 3))

        self.assertTrue(topology.isdihedral(0, 1, 2, 3))
        self.assertFalse(topology.isdihedral(0, 1, 3, 2))

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

        topology.remove(3)
        self.assertEqual(len(topology), 3)


if __name__ == '__main__':
    unittest.main()
