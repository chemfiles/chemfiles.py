import copy
import unittest

import numpy as np

from chemfiles import ChemfilesError, Property


class TestProperty(unittest.TestCase):
    def test_bool(self):
        prop = Property(False)
        self.assertEqual(prop.get(), False)

    def test_number(self):
        prop = Property(22)
        self.assertEqual(prop.get(), 22.0)

        prop = Property(42.2)
        self.assertEqual(prop.get(), 42.2)

    def test_string(self):
        prop = Property("foo")
        self.assertEqual(prop.get(), "foo")

    def test_vector3d(self):
        prop = Property((3, 4, 5))
        self.assertEqual(prop.get(), (3, 4, 5))

        prop = Property([3, 4, 5])
        self.assertEqual(prop.get(), (3, 4, 5))

        prop = Property(np.array([3, 4, 5]))
        self.assertEqual(prop.get(), (3, 4, 5))

    def test_bad(self):
        with self.assertRaises(ChemfilesError):
            _ = Property(ArithmeticError)


if __name__ == "__main__":
    unittest.main()
