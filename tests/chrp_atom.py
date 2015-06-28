#!/usr/bin/env python
# -* coding: utf-8 -*

from chemharp import Atom
import unittest


class AtomTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AtomTest, self).__init__(*args, **kwargs)
        self.atom = Atom("He")

    def test_mass(self):
        self.assertAlmostEqual(self.atom.mass(), 4.00260210037, delta=1e-10)
        self.atom.mass(678)
        self.assertAlmostEqual(self.atom.mass(), 678, delta=1e-10)

    def test_charge(self):
        self.assertEqual(self.atom.charge(), 0)
        self.atom.charge(-1.5)
        self.assertEqual(self.atom.charge(), -1.5)

    def test_names(self):
        self.assertEqual(self.atom.name(), "He")
        self.atom.name("Zn")
        self.assertEqual(self.atom.name(), "Zn")
        self.assertEqual(self.atom.full_name(), "Zinc")

    def test_radii(self):
        self.assertAlmostEqual(self.atom.vdw_radius(), 1.4, delta=1e-6)
        self.assertAlmostEqual(self.atom.covalent_radius(), 0.32, delta=1e-6)

    def test_atomic_number(self):
        self.atom.name("Zn")
        self.assertEqual(self.atom.atomic_number(), 30)


if __name__ == '__main__':
    unittest.main()
