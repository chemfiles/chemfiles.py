# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import numpy as np
import os
from ctypes import ArgumentError

from chemfiles import Trajectory, Topology, Frame, UnitCell, Atom
from chemfiles import ChemfilesError

from _utils import remove_warnings


def get_data_path(data):
    root = os.path.dirname(__file__)
    return os.path.join(root, "data", data)


class TestTrajectory(unittest.TestCase):
    def test_errors(self):
        with remove_warnings:
            self.assertRaises(ChemfilesError, Trajectory, get_data_path("not-here.xyz"))
            self.assertRaises(ChemfilesError, Trajectory, get_data_path("empty.unknown"))

            with Trajectory("test-tmp.xyz", "w") as trajectory:
                self.assertRaises(ArgumentError, trajectory.write, None)

            os.unlink("test-tmp.xyz")

    def test_read(self):
        trajectory = Trajectory(get_data_path("water.xyz"))

        self.assertEqual(trajectory.nsteps, 100)
        self.assertEqual(trajectory.path, get_data_path("water.xyz"))

        frame = trajectory.read()
        self.assertEqual(len(frame.atoms), 297)

        self.assertEqual(
            frame.positions[0].all(),
            np.array([0.417219, 8.303366, 11.737172]).all()
        )
        self.assertEqual(
            frame.positions[124].all(),
            np.array([5.099554, -0.045104, 14.153846]).all()
        )

        self.assertEqual(len(frame.atoms), 297)
        self.assertEqual(frame.atoms[0].name, "O")
        self.assertEqual(frame.atoms[1].name, "H")

        trajectory.set_cell(UnitCell(30, 30, 30))
        frame = trajectory.read_step(41)
        self.assertEqual(frame.cell.lengths, (30.0, 30.0, 30.0))

        self.assertEqual(
            frame.positions[0].all(),
            np.array([0.761277, 8.106125, 10.622949]).all()
        )
        self.assertEqual(
            frame.positions[124].all(),
            np.array([5.13242, 0.079862, 14.194161]).all()
        )

        self.assertEqual(len(frame.atoms), 297)
        self.assertEqual(frame.topology.bonds_count(), 0)

        frame.guess_bonds()
        self.assertEqual(frame.topology.bonds_count(), 181)
        self.assertEqual(frame.topology.angles_count(), 87)

        topology = Topology()
        for i in range(297):
            topology.atoms.append(Atom("Cs"))

        trajectory.set_topology(topology)
        frame = trajectory.read_step(10)
        self.assertEqual(frame.atoms[10].name, "Cs")

        trajectory.set_topology(get_data_path("topology.xyz"), "XYZ")
        frame = trajectory.read()
        self.assertEqual(frame.atoms[100].name, "Rd")

    def test_protocols(self):
        with Trajectory(get_data_path("water.xyz")) as trajectory:
            for frame in trajectory:
                self.assertEqual(len(frame.atoms), 297)

    def test_close(self):
        trajectory = Trajectory(get_data_path("water.xyz"))
        trajectory.close()
        self.assertRaises(ChemfilesError, trajectory.read)

    def test_write(self):
        frame = Frame()
        for i in range(4):
            frame.add_atom(Atom("X"), [1, 2, 3])

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


if __name__ == "__main__":
    unittest.main()
