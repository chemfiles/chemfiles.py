# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy
import numpy as np

from chemfiles import Residue, ChemfilesError


class TestResidue(unittest.TestCase):
    def test_copy(self):
        residue = Residue("bar")
        residue.add_atom(7)
        cloned = copy.copy(residue)

        self.assertEqual(residue.natoms(), 1)
        self.assertEqual(cloned.natoms(), 1)

        residue.add_atom(2)
        self.assertEqual(residue.natoms(), 2)
        self.assertEqual(cloned.natoms(), 1)

    def test_name(self):
        residue = Residue('bar')
        self.assertEqual(residue.name(), 'bar')

    def test_id(self):
        residue = Residue('bar')
        self.assertRaises(ChemfilesError, residue.id)

        residue = Residue('bar', 45)
        self.assertEqual(residue.id(), 45)

    def test_atoms(self):
        residue = Residue('')
        residue.add_atom(3)
        residue.add_atom(4)
        residue.add_atom(1)

        self.assertEqual(residue.natoms(), 3)
        self.assertEqual(len(residue), 3)

        self.assertTrue(residue.contains(3))
        self.assertFalse(residue.contains(6))

        self.assertEqual(
            residue.atoms().all(),
            np.array([1, 3, 4]).all()
        )


if __name__ == '__main__':
    unittest.main()
