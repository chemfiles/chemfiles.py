# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import numpy as np
import os
from ctypes import ArgumentError

from chemfiles import Trajectory, Topology, Frame, UnitCell, Atom
from chemfiles import ChemfilesException


class TestTrajectory(unittest.TestCase):
    def test_errors(self):
        self.assertRaises(
            ChemfilesException,
            Trajectory,
            os.path.join("data", "not-here.xyz")
        )
        self.assertRaises(
            ChemfilesException,
            Trajectory,
            os.path.join("data", "empty.unknown")
        )

        with Trajectory("test-tmp.xyz", "w") as trajectory:
            self.assertRaises(ArgumentError, trajectory.write, None)

        os.unlink("test-tmp.xyz")

    def test_read(self):
        trajectory = Trajectory(os.path.join("data", "water.xyz"))

        self.assertEqual(trajectory.nsteps(), 100)

        frame = trajectory.read()
        self.assertEqual(frame.natoms(), 297)

        positions = frame.positions()
        self.assertEqual(
            positions[0].all(),
            np.array([0.417219, 8.303366, 11.737172]).all()
        )
        self.assertEqual(
            positions[124].all(),
            np.array([5.099554, -0.045104, 14.153846]).all()
        )

        topology = frame.topology()
        self.assertEqual(topology.natoms(), 297)
        self.assertEqual(topology.atom(0).name(), "O")
        self.assertEqual(topology.atom(1).name(), "H")

        trajectory.set_cell(UnitCell(30, 30, 30))
        trajectory.read_step(41, frame)
        self.assertEqual(frame.cell().lengths(), (30.0, 30.0, 30.0))

        positions = frame.positions()
        self.assertEqual(
            positions[0].all(),
            np.array([0.761277, 8.106125, 10.622949]).all()
        )
        self.assertEqual(
            positions[124].all(),
            np.array([5.13242, 0.079862, 14.194161]).all()
        )

        topology = frame.topology()
        self.assertEqual(topology.natoms(), 297)
        self.assertEqual(topology.bonds_count(), 0)

        frame.guess_topology()
        topology = frame.topology()
        self.assertEqual(topology.bonds_count(), 181)
        self.assertEqual(topology.angles_count(), 87)

        topology = Topology()
        for i in range(297):
            topology.add_atom(Atom("Cs"))

        trajectory.set_topology(topology)
        frame = trajectory.read_step(10)
        self.assertEqual(frame.atom(10).name(), "Cs")

        trajectory.set_topology(os.path.join("data", "topology.xyz"), "XYZ")
        frame = trajectory.read()
        self.assertEqual(frame.atom(100).name(), "Rd")

    def test_protocols(self):
        with Trajectory(os.path.join("data", "water.xyz")) as trajectory:
            for frame in trajectory:
                self.assertEqual(frame.natoms(), 297)

    def test_close(self):
        trajectory = Trajectory(os.path.join("data", "water.xyz"))
        trajectory.close()
        self.assertRaises(ChemfilesException, trajectory.read)

    def test_write(self):
        frame = Frame()
        frame.resize(4)
        positions = frame.positions()
        topology = Topology()
        for i in range(4):
            positions[i] = [1, 2, 3]
            topology.add_atom(Atom("X"))

        frame.set_topology(topology)
        with Trajectory("test-tmp.xyz", "w") as fd:
            fd.write(frame)

        expected_content = """4
Written by the chemfiles library
X 1 2 3
X 1 2 3
X 1 2 3
X 1 2 3
"""
        with open("test-tmp.xyz") as fd:
            self.assertEqual(fd.read(), expected_content)

        os.unlink("test-tmp.xyz")


if __name__ == '__main__':
    unittest.main()
