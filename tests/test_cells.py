# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import numpy as np

from chemharp import UnitCell, CellType
from chemharp import ChemharpException
from chemharp import logging


class TestUnitCell(unittest.TestCase):
    def test_lengths(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.lengths(), (3.0, 4.0, 5.0))
        cell.set_lengths(10, 11, 12)
        self.assertEqual(cell.lengths(), (10.0, 11.0, 12.0))

    def test_angles(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.angles(), (90.0, 90.0, 90.0))

        logging.set_log_level(logging.LogLevel.NONE)
        self.assertRaises(ChemharpException, cell.set_angles, 80, 89, 110)
        logging.set_log_level(logging.LogLevel.WARNING)

        cell.set_type(CellType.Triclinic)
        cell.set_angles(80, 89, 110)
        self.assertEqual(cell.angles(), (80.0, 89.0, 110.0))

    def test_volume(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.volume(), 3 * 4 * 5)

    def test_matrix(self):
        cell = UnitCell(3, 4, 5)
        res = np.array([[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 4.0]])
        self.assertEqual(cell.matrix().all(), res.all())

    def test_type(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.type(), CellType.Orthorombic)
        cell.set_type(CellType.Infinite)
        self.assertEqual(cell.type(), CellType.Infinite)

        cell = UnitCell(3, 4, 5, 100, 120, 130)
        self.assertEqual(cell.type(), CellType.Triclinic)

    def test_periodicity(self):
        cell = UnitCell(3, 4, 5)
        self.assertEqual(cell.periodicity(), (True, True, True))
        cell.set_periodicity(False, True, False)
        self.assertEqual(cell.periodicity(), (False, True, False))


if __name__ == '__main__':
    unittest.main()
