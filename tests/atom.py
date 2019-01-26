# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy

from chemfiles import Atom, ChemfilesError
from utils import remove_warnings


class TestAtom(unittest.TestCase):
    def test_copy(self):
        atom = Atom("He")
        cloned = copy.copy(atom)

        self.assertEqual(atom.name(), "He")
        self.assertEqual(cloned.name(), "He")

        atom.set_name("Zn")
        self.assertEqual(atom.name(), "Zn")
        self.assertEqual(cloned.name(), "He")

    def test_name(self):
        atom = Atom("He")
        self.assertEqual(atom.name(), "He")
        self.assertEqual(atom.full_name(), "Helium")

        atom.set_name("Zn")
        self.assertEqual(atom.name(), "Zn")

    def test_type(self):
        atom = Atom("He")
        self.assertEqual(atom.type(), "He")
        self.assertEqual(atom.full_name(), "Helium")

        atom.set_type("Zn")
        self.assertEqual(atom.type(), "Zn")
        self.assertEqual(atom.full_name(), "Zinc")

        atom = Atom("He2", "H")
        self.assertEqual(atom.name(), "He2")
        self.assertEqual(atom.type(), "H")

    def test_mass(self):
        atom = Atom("He")
        self.assertAlmostEqual(atom.mass(), 4.002602, 6)
        atom.set_mass(1.0)
        self.assertEqual(atom.mass(), 1.0)

    def test_charge(self):
        atom = Atom("He")
        self.assertEqual(atom.charge(), 0.0)
        atom.set_charge(-1.5)
        self.assertEqual(atom.charge(), -1.5)

    def test_radii(self):
        self.assertAlmostEqual(Atom("He").vdw_radius(), 1.4, 2)
        self.assertAlmostEqual(Atom("He").covalent_radius(), 0.32, 3)

        self.assertEqual(Atom("H1").vdw_radius(), 0)
        self.assertEqual(Atom("H1").covalent_radius(), 0)

    def test_atomic_number(self):
        self.assertEqual(Atom("He").atomic_number(), 2)
        self.assertEqual(Atom("H1").atomic_number(), 0)

    def test_property(self):
        atom = Atom("He")

        atom.set("foo", 3)
        self.assertEqual(atom.get("foo"), 3.0)

        atom.set("foo", False)
        self.assertEqual(atom.get("foo"), False)

        with remove_warnings:
            self.assertRaises(ChemfilesError, atom.get, "bar")


if __name__ == "__main__":
    unittest.main()
