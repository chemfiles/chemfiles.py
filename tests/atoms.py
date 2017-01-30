# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import copy

from chemfiles import Atom


class TestAtom(unittest.TestCase):
    def test_copy(self):
        atom = Atom("He")
        cloned = copy.copy(atom)

        self.assertEqual(atom.name(), 'He')
        self.assertEqual(cloned.name(), 'He')

        atom.set_name("Zn")
        self.assertEqual(atom.name(), 'Zn')
        self.assertEqual(cloned.name(), 'He')

    def test_name(self):
        atom = Atom("He")
        self.assertEqual(atom.name(), 'He')
        self.assertEqual(atom.full_name(), 'Helium')

        atom.set_name("Zn")
        self.assertEqual(atom.name(), 'Zn')

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
        atom = Atom("He")
        self.assertAlmostEqual(atom.vdw_radius(), 1.4, 2)
        self.assertAlmostEqual(atom.covalent_radius(), 0.32, 3)

    def test_atomic_number(self):
        atom = Atom("He")
        self.assertEqual(atom.atomic_number(), 2)


if __name__ == '__main__':
    unittest.main()
