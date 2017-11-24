# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy
import numpy as np

from chemfiles import Frame, UnitCell, Topology, Atom


class TestFrame(unittest.TestCase):
    def test_copy(self):
        frame = Frame()
        cloned = copy.copy(frame)

        self.assertEqual(frame.natoms(), 0)
        self.assertEqual(cloned.natoms(), 0)

        frame.resize(6)
        self.assertEqual(frame.natoms(), 6)
        self.assertEqual(cloned.natoms(), 0)

    def test_natoms(self):
        frame = Frame()
        self.assertEqual(frame.natoms(), 0)
        self.assertEqual(len(frame), 0)

        frame.resize(4)
        self.assertEqual(frame.natoms(), 4)
        self.assertEqual(len(frame), 4)

        frame.remove(2)
        self.assertEqual(frame.natoms(), 3)
        self.assertEqual(len(frame), 3)

    def test_add_atom(self):
        frame = Frame()
        frame.add_atom(Atom("F"), (3, 4, 5))
        self.assertEqual(len(frame), 1)
        self.assertEqual(list(frame.positions()[0]), [3, 4, 5])

        frame.add_velocities()
        frame.add_atom(Atom("F"), (-3, -4, 5), (1, 0, 1))
        self.assertEqual(list(frame.positions()[1]), [-3, -4, 5])
        self.assertEqual(list(frame.velocities()[1]), [1, 0, 1])

    def test_positions(self):
        frame = Frame()
        frame.resize(4)

        expected = np.array([[1.0, 2.0, 3.0],
                             [4.0, 5.0, 6.0],
                             [7.0, 8.0, 9.0],
                             [10.0, 11.0, 12.0]], np.float64)
        positions = frame.positions()
        np.copyto(positions, expected)
        self.assertEqual(frame.positions().all(), expected.all())

        positions[3, 2] = 42
        self.assertEqual(frame.positions()[3, 2], 42)

        # Checking empty frame positions access
        frame = Frame()
        positions = frame.positions()

    def test_velocities(self):
        frame = Frame()
        frame.resize(4)

        self.assertFalse(frame.has_velocities())
        frame.add_velocities()
        self.assertTrue(frame.has_velocities())

        expected = np.array([[1.0, 2.0, 3.0],
                             [4.0, 5.0, 6.0],
                             [7.0, 8.0, 9.0],
                             [10.0, 11.0, 12.0]], np.float64)
        velocities = frame.velocities()
        np.copyto(velocities, expected)
        self.assertEqual(frame.velocities().all(), expected.all())

        velocities[3, 2] = 42
        self.assertEqual(frame.velocities()[3, 2], 42)

        # Checking empty frame velocities access
        frame = Frame()
        frame.add_velocities()
        velocities = frame.velocities()

    def test_cell(self):
        frame = Frame()
        cell = UnitCell(1, 2, 4)

        frame.set_cell(cell)
        self.assertEqual(frame.cell().lengths(), cell.lengths())
        self.assertEqual(frame.cell().angles(), cell.angles())
        self.assertEqual(frame.cell().shape(), cell.shape())

    def test_topology(self):
        frame = Frame()
        frame.resize(2)

        topology = Topology()
        topology.add_atom(Atom("Zn"))
        topology.add_atom(Atom("Ar"))

        frame.set_topology(topology)

        topology = frame.topology()
        self.assertEqual(topology.atom(0).name(), "Zn")
        self.assertEqual(topology.atom(1).name(), "Ar")

        self.assertEqual(frame.atom(0).name(), "Zn")
        self.assertEqual(frame.atom(1).name(), "Ar")

    def test_step(self):
        frame = Frame()
        self.assertEqual(frame.step(), 0)
        frame.set_step(42)
        self.assertEqual(frame.step(), 42)

    def test_out_of_bounds(self):
        frame = Frame()
        frame.resize(3)
        frame.atom(2)
        self.assertRaises(IndexError, frame.atom, 6)

    def test_iter(self):
        frame = Frame()
        frame.resize(3)
        i = 0
        for atom in frame:
            self.assertEqual(atom.name(), "")
            i += 1
        self.assertEqual(i, 3)


if __name__ == '__main__':
    unittest.main()
