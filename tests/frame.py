# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy
import math
import numpy as np

from chemfiles import Frame, UnitCell, Topology, Atom, Residue, ChemfilesError
from chemfiles import BondOrder, CellShape
from _utils import remove_warnings


class TestFrame(unittest.TestCase):
    def test_repr(self):
        frame = Frame()
        self.assertEqual(frame.__repr__(), "Frame with 0 atoms")
        frame.resize(4)
        self.assertEqual(frame.__repr__(), "Frame with 4 atoms")

        self.assertEqual(
            frame.atoms.__repr__(), "[Atom(''), Atom(''), Atom(''), Atom('')]"
        )

    def test_copy(self):
        frame = Frame()
        cloned = copy.copy(frame)

        self.assertEqual(len(frame.atoms), 0)
        self.assertEqual(len(cloned.atoms), 0)

        frame.resize(6)
        self.assertEqual(len(frame.atoms), 6)
        self.assertEqual(len(cloned.atoms), 0)

    def test_atoms_count(self):
        frame = Frame()
        self.assertEqual(len(frame.atoms), 0)

        frame.resize(4)
        self.assertEqual(len(frame.atoms), 4)

        frame.remove(2)
        self.assertEqual(len(frame.atoms), 3)

    def test_add_atom(self):
        frame = Frame()
        frame.add_atom(Atom("F"), (3, 4, 5))
        self.assertEqual(len(frame.atoms), 1)
        self.assertEqual(list(frame.positions[0]), [3, 4, 5])

        frame.add_velocities()
        frame.add_atom(Atom("F"), (-3, -4, 5), (1, 0, 1))
        self.assertEqual(list(frame.positions[1]), [-3, -4, 5])
        self.assertEqual(list(frame.velocities[1]), [1, 0, 1])

    def test_positions(self):
        frame = Frame()
        frame.resize(4)

        expected = np.array(
            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [10.0, 11.0, 12.0]],
            np.float64,
        )
        np.copyto(frame.positions, expected)
        self.assertEqual(frame.positions.all(), expected.all())

        frame.positions[3, 2] = 42
        self.assertEqual(frame.positions[3, 2], 42)

        # Checking empty frame positions access
        _ = Frame().positions

    def test_velocities(self):
        frame = Frame()
        frame.resize(4)

        self.assertFalse(frame.has_velocities())
        frame.add_velocities()
        self.assertTrue(frame.has_velocities())

        expected = np.array(
            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [10.0, 11.0, 12.0]],
            np.float64,
        )
        np.copyto(frame.velocities, expected)
        self.assertEqual(frame.velocities.all(), expected.all())

        frame.velocities[3, 2] = 42
        self.assertEqual(frame.velocities[3, 2], 42)

        # Checking empty frame velocities access
        frame = Frame()
        frame.add_velocities()
        _ = frame.velocities

    def test_cell(self):
        frame = Frame()
        frame.cell = UnitCell([1, 2, 4])
        self.assertEqual(frame.cell.lengths, (1, 2, 4))
        self.assertEqual(frame.cell.angles, (90, 90, 90))
        self.assertEqual(frame.cell.shape, CellShape.Orthorhombic)

        frame.cell.lengths = (3, 4, 5)
        self.assertEqual(frame.cell.lengths, (3, 4, 5))

    def test_topology(self):
        frame = Frame()
        frame.resize(2)

        topology = Topology()
        topology.atoms.append(Atom("Zn"))
        topology.atoms.append(Atom("Ar"))

        frame.topology = topology
        self.assertEqual(frame.atoms[0].name, "Zn")
        self.assertEqual(frame.atoms[1].name, "Ar")

    def test_step(self):
        frame = Frame()
        self.assertEqual(frame.step, 0)
        frame.step = 42
        self.assertEqual(frame.step, 42)

    def test_out_of_bounds(self):
        frame = Frame()
        frame.resize(3)
        _ = frame.atoms[2]
        with self.assertRaises(IndexError):
            _ = frame.atoms[6]

    def test_iter(self):
        frame = Frame()
        frame.resize(3)

        for i, atom in enumerate(frame.atoms):
            self.assertEqual(atom.name, "")
        self.assertEqual(i, 2)

        for i, atom in enumerate(frame.topology.atoms):
            self.assertEqual(atom.name, "")
        self.assertEqual(i, 2)

    def test_property(self):
        frame = Frame()

        frame["foo"] = 3
        self.assertEqual(frame["foo"], 3.0)

        frame["foo"] = False
        self.assertEqual(frame["foo"], False)

        with remove_warnings:
            with self.assertRaises(ChemfilesError):
                _ = frame["bar"]

            with self.assertRaises(ChemfilesError):
                frame[3] = "test"

            with self.assertRaises(ChemfilesError):
                _ = frame[3]

        # Check that enabling indexing/__getitem__ did not enable iteration
        with self.assertRaises(TypeError):
            for i in frame:
                pass

        frame["bar"] = "baz"

        self.assertEqual(frame.properties_count(), 2)
        self.assertEqual(set(frame.list_properties()), {"bar", "foo"})

    def test_distance(self):
        frame = Frame()
        frame.cell = UnitCell([3.0, 4.0, 5.0])
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (1, 2, 6))

        self.assertEqual(frame.distance(0, 1), math.sqrt(6.0))

    def test_angle(self):
        frame = Frame()
        frame.add_atom(Atom(""), (1, 0, 0))
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (0, 1, 0))

        self.assertEqual(frame.angle(0, 1, 2), math.pi / 2.0)

    def test_dihedral(self):
        frame = Frame()
        frame.add_atom(Atom(""), (1, 0, 0))
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (0, 1, 0))
        frame.add_atom(Atom(""), (-1, 1, 0))

        self.assertEqual(frame.dihedral(0, 1, 2, 3), math.pi)

    def test_out_of_plane(self):
        frame = Frame()
        frame.add_atom(Atom(""), (1, 0, 0))
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (0, 1, 0))
        frame.add_atom(Atom(""), (0, 0, 3))

        self.assertEqual(frame.out_of_plane(1, 3, 0, 2), 3.0)

    def test_bonds(self):
        frame = Frame()
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (0, 0, 0))
        frame.add_atom(Atom(""), (0, 0, 0))

        frame.add_bond(0, 1)
        frame.add_bond(3, 4)
        frame.add_bond(2, 1, BondOrder.Quintuplet)

        self.assertEqual(
            frame.topology.bonds.all(), np.array([[0, 1], [1, 2], [3, 4]]).all()
        )

        self.assertEqual(
            frame.topology.bonds_orders,
            [BondOrder.Unknown, BondOrder.Quintuplet, BondOrder.Unknown],
        )

        frame.remove_bond(3, 4)
        # Also try to remove non-existing bonds
        frame.remove_bond(3, 4)
        frame.remove_bond(0, 4)

        self.assertEqual(frame.topology.bonds.all(), np.array([[0, 1], [1, 2]]).all())

        frame.clear_bonds()
        self.assertEqual(frame.topology.bonds_count(), 0)

    def test_residues(self):
        frame = Frame()
        frame.add_residue(Residue("Foo"))
        frame.add_residue(Residue("Foo"))
        frame.add_residue(Residue("Foo"))

        self.assertEqual(len(frame.topology.residues), 3)
        self.assertEqual(frame.topology.residues[0].name, "Foo")


if __name__ == "__main__":
    unittest.main()
