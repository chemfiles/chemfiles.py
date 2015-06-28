#!/usr/bin/env python
# -* coding: utf-8 -*

from chemharp import UnitCell, CellType
import unittest
import numpy


class UnitCellTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UnitCellTest, self).__init__(*args, **kwargs)
        self.cell = UnitCell(2, 3, 4)

    def test_lengthes(self):
        self.assertEqual(self.cell.a(), 2)
        self.assertEqual(self.cell.b(), 3)
        self.assertEqual(self.cell.c(), 4)
        self.cell.a(10)
        self.cell.b(20)
        self.cell.c(30)
        self.assertEqual(self.cell.a(), 10)
        self.assertEqual(self.cell.b(), 20)
        self.assertEqual(self.cell.c(), 30)

    def test_angles(self):
        self.assertEqual(self.cell.alpha(), 90)
        self.assertEqual(self.cell.beta(), 90)
        self.assertEqual(self.cell.gamma(), 90)

        self.assertRaises(UserWarning, self.cell.alpha, 80)
        self.assertRaises(UserWarning, self.cell.beta, 89)
        self.assertRaises(UserWarning, self.cell.gamma, 120)

        self.cell.type(CellType.TRICLINIC)
        self.cell.alpha(80)
        self.cell.beta(89)
        self.cell.gamma(120)

        self.assertEqual(self.cell.alpha(), 80)
        self.assertEqual(self.cell.beta(), 89)
        self.assertEqual(self.cell.gamma(), 120)

    def test_volume(self):
        self.assertEqual(self.cell.volume(), 2*3*4)

    def test_type(self):
        self.assertEqual(self.cell.type(), CellType.ORTHOROMBIC)
        self.cell.type(CellType.TRICLINIC)
        self.assertEqual(self.cell.type(), CellType.TRICLINIC)

    def test_matrix(self):
        result = numpy.array([[10.0, 0.0, 0.0],
                              [0.0, 20.0, 0.0],
                              [0.0, 0.0, 30.0]])
        self.assertEqual(self.cell.matricial().all(), result.all())

    def test_periodic(self):
        self.assertTrue(self.cell.periodic_x())
        self.assertTrue(self.cell.periodic_y())
        self.assertTrue(self.cell.periodic_z())
        self.assertTrue(self.cell.full_periodic())

        self.cell.periodic_x(False)
        self.assertFalse(self.cell.full_periodic())

        self.cell.periodic_y(False)
        self.cell.periodic_z(False)

        self.assertFalse(self.cell.periodic_x())
        self.assertFalse(self.cell.periodic_y())
        self.assertFalse(self.cell.periodic_z())


if __name__ == '__main__':
    unittest.main()
