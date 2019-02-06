# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy
import numpy as np

from chemfiles import Residue, ChemfilesError
from _utils import remove_warnings


class TestResidue(unittest.TestCase):
    def test_copy(self):
        residue = Residue("bar")
        residue.atoms.append(7)
        cloned = copy.copy(residue)

        self.assertEqual(len(residue.atoms), 1)
        self.assertEqual(len(cloned.atoms), 1)

        residue.atoms.append(2)
        self.assertEqual(len(residue.atoms), 2)
        self.assertEqual(len(cloned.atoms), 1)

    def test_name(self):
        residue = Residue("bar")
        self.assertEqual(residue.name, "bar")

    def test_id(self):
        residue = Residue("bar")
        with remove_warnings:
            with self.assertRaises(ChemfilesError):
                _ = residue.id

        residue = Residue("bar", 45)
        self.assertEqual(residue.id, 45)

    def test_atoms(self):
        residue = Residue("")
        residue.atoms.append(3)
        residue.atoms.append(4)
        residue.atoms.append(1)

        self.assertEqual(len(residue.atoms), 3)
        self.assertTrue(3 in residue.atoms)
        self.assertFalse(6 in residue.atoms)

        self.assertEqual(list(residue.atoms), [1, 3, 4])

        atoms = residue.atoms
        _ = atoms[0]
        # Check for __contains__ with a cache
        self.assertTrue(atoms.indexes is not None)
        self.assertTrue(3 in atoms)
        self.assertFalse(6 in atoms)

    def test_property(self):
        residue = Residue("ALA")

        residue["foo"] = 3
        self.assertEqual(residue["foo"], 3.0)

        residue["foo"] = False
        self.assertEqual(residue["foo"], False)

        with remove_warnings:
            with self.assertRaises(ChemfilesError):
                _ = residue["bar"]

        residue["bar"] = "baz"

        self.assertEqual(residue.properties_count(), 2)
        self.assertEqual(residue.list_properties(), ["bar", "foo"])


if __name__ == "__main__":
    unittest.main()
