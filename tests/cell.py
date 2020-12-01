# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy

from chemfiles import UnitCell, CellShape
from chemfiles import ChemfilesError
from _utils import remove_warnings


class TestUnitCell(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(UnitCell(3, 4, 5).__repr__(), "UnitCell(3, 4, 5, 90, 90, 90)")
        self.assertEqual(UnitCell(3, 4, 5, 89.015, 120, 112).__repr__(), "UnitCell(3, 4, 5, 89.015, 120, 112)")

    def test_copy(self):
        cell = UnitCell(3, 4, 5)
        cloned = copy.copy(cell)

        self.assertEqual(cell.lengths, (3.0, 4.0, 5.0))
        self.assertEqual(cloned.lengths, (3.0, 4.0, 5.0))

        cell.lengths = 10, 11, 12
        self.assertEqual(cell.lengths, (10.0, 11.0, 12.0))
        self.assertEqual(cloned.lengths, (3.0, 4.0, 5.0))

    def test_lengths(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.lengths, (3.0, 4.0, 5.0))
        cell.lengths = [10, 11, 12]
        self.assertEqual(cell.lengths, (10.0, 11.0, 12.0))

    def test_angles(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.angles, (90.0, 90.0, 90.0))

        self.assertEqual(cell.shape, CellShape.Orthorhombic)
        with remove_warnings:
            with self.assertRaises(ChemfilesError):
                cell.angles = [80, 89, 110]

        cell.shape = CellShape.Triclinic
        cell.angles = [80, 89, 110]
        self.assertEqual(cell.angles, (80.0, 89.0, 110.0))

    def test_volume(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.volume, 3 * 4 * 5)

    def test_matrix(self):
        cell = UnitCell(3, 4, 5)
        expected = [(3, 0, 0), (0, 4, 0), (0, 0, 5)]
        matrix = cell.matrix
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(matrix[i][j], expected[i][j])

    def test_shape(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.shape, CellShape.Orthorhombic)
        cell.shape = CellShape.Triclinic
        self.assertEqual(cell.shape, CellShape.Triclinic)

        cell = UnitCell(3, 4, 5, 100, 120, 130)
        self.assertEqual(cell.shape, CellShape.Triclinic)

    def test_wrap(self):
        cell = UnitCell(3, 4, 5)

        wrapped = cell.wrap((1, 5, -5.5))

        self.assertEqual(wrapped[0], 1.0)
        self.assertEqual(wrapped[1], 1.0)
        self.assertEqual(wrapped[2], -0.5)


if __name__ == "__main__":
    unittest.main()
