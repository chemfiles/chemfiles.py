# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import numpy as np

from chemfiles import Frame, UnitCell, Topology, Atom


class TestFrame(unittest.TestCase):
    def test_natoms(self):
        frame = Frame()
        self.assertEqual(frame.natoms(), 0)
        self.assertEqual(len(frame), 0)

        frame.resize(4)
        self.assertEqual(frame.natoms(), 4)
        self.assertEqual(len(frame), 4)

        frame = Frame(4)
        self.assertEqual(frame.natoms(), 4)
        self.assertEqual(len(frame), 4)

    def test_positions(self):
        frame = Frame(4)

        expected = np.array([[1.0, 2.0, 3.0],
                             [4.0, 5.0, 6.0],
                             [7.0, 8.0, 9.0],
                             [10.0, 11.0, 12.0]], np.float32)
        positions = frame.positions()
        np.copyto(positions, expected)
        self.assertEqual(positions.all(), expected.all())

        positions[3, 2] = 42
        self.assertEqual(frame.positions()[3, 2], 42)

    def test_velocities(self):
        frame = Frame(4)

        self.assertFalse(frame.has_velocities())
        frame.add_velocities()
        self.assertTrue(frame.has_velocities())

        expected = np.array([[1.0, 2.0, 3.0],
                             [4.0, 5.0, 6.0],
                             [7.0, 8.0, 9.0],
                             [10.0, 11.0, 12.0]], np.float32)
        velocities = frame.velocities()
        np.copyto(velocities, expected)
        self.assertEqual(frame.velocities().all(), expected.all())

    def test_cell(self):
        frame = Frame(0)
        cell = UnitCell(1, 2, 4)

        frame.set_cell(cell)
        self.assertEqual(frame.cell().lengths(), cell.lengths())
        self.assertEqual(frame.cell().angles(), cell.angles())
        self.assertEqual(frame.cell().type(), cell.type())

    def test_topology(self):
        frame = Frame()
        topology = Topology()

        topology.append(Atom("Zn"))
        topology.append(Atom("Ar"))

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


if __name__ == '__main__':
    unittest.main()
