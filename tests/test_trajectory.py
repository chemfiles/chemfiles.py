# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import numpy as np
import os

from chemfiles import Trajectory, Topology, Frame, UnitCell, Atom
from chemfiles import ChemfilesException, logging

DATA = os.path.join(os.path.dirname(__file__), "data")


class TestTrajectory(unittest.TestCase):
    def test_errors(self):
        logging.set_log_level(logging.LogLevel.NONE)
        self.assertRaises(
            ChemfilesException, Trajectory, os.path.join(DATA, "not-here.xyz")
        )
        self.assertRaises(
            ChemfilesException, Trajectory, os.path.join(DATA, "empty.unknown")
        )
        logging.set_log_level(logging.LogLevel.WARNING)

    def test_read(self):
        trajectory = Trajectory(os.path.join(DATA, "water.xyz"))

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
        frame = trajectory.read_step(41)
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
        a = Atom("Cs")
        for i in range(297):
            topology.append(a)

        trajectory.set_topology(topology)
        frame = trajectory.read_step(10)
        self.assertEqual(frame.atom(10).name(), "Cs")

        trajectory.set_topology_file(os.path.join(DATA, "topology.xyz"))
        frame = trajectory.read()
        self.assertEqual(frame.atom(100).name(), "Rd")

    def test_write(self):
        positions = np.zeros((4, 3), np.float32)
        topology = Topology()
        for i in range(4):
            positions[i] = [1, 2, 3]
            topology.append(Atom("X"))

        frame_1 = Frame()
        frame_1.set_positions(positions)
        frame_1.set_topology(topology)

        positions = np.zeros((6, 3), np.float32)
        topology = Topology()
        for i in range(6):
            positions[i] = [4, 5, 6]
            topology.append(Atom("X"))

        frame_2 = Frame()
        frame_2.set_positions(positions)
        frame_2.set_topology(topology)

        fd = Trajectory("test-tmp.xyz", "w")
        fd.write(frame_1)
        fd.write(frame_2)
        fd.sync()

        expected_content = "\n".join(["4",
                                      "Written by the chemfiles library",
                                      "X 1 2 3",
                                      "X 1 2 3",
                                      "X 1 2 3",
                                      "X 1 2 3",
                                      "6",
                                      "Written by the chemfiles library",
                                      "X 4 5 6",
                                      "X 4 5 6",
                                      "X 4 5 6",
                                      "X 4 5 6",
                                      "X 4 5 6",
                                      "X 4 5 6",
                                      ""])

        with open("test-tmp.xyz") as fd:
            self.assertEqual(fd.read(), expected_content)

        os.unlink("test-tmp.xyz")

    def test_molfiles(self):
        trajectory = Trajectory(os.path.join(DATA, "water.trr"))
        self.assertEqual(trajectory.nsteps(), 100)


if __name__ == '__main__':
    unittest.main()
