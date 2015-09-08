# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
from chemharp import Atom


class TestAtom(unittest.TestCase):
    def test_name(self):
        a = Atom("He")
        self.assertEqual(a.name(), 'He')
        self.assertEqual(a.full_name(), 'Helium')

        a.set_name("Zn")
        self.assertEqual(a.name(), 'Zn')
        self.assertEqual(a.full_name(), 'Zinc')

    def test_mass(self):
        a = Atom("He")
        self.assertAlmostEqual(a.mass(), 4.002602, 6)
        a.set_mass(1.0)
        self.assertEqual(a.mass(), 1.0)

    def test_charge(self):
        a = Atom("He")
        self.assertEqual(a.charge(), 0.0)
        a.set_charge(-1.5)
        self.assertEqual(a.charge(), -1.5)

    def test_radii(self):
        a = Atom("He")
        self.assertAlmostEqual(a.vdw_radius(), 1.4, 2)
        self.assertAlmostEqual(a.covalent_radius(), 0.32, 3)

    def test_atomic_number(self):
        a = Atom("He")
        self.assertEqual(a.atomic_number(), 2)
