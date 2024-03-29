import copy
import unittest

from chemfiles import Atom, Frame, Selection, Topology


def testing_frame():
    frame = Frame()

    frame.add_atom(Atom("H"), [0, 0, 0])
    frame.add_atom(Atom("O"), [0, 0, 0])
    frame.add_atom(Atom("O"), [0, 0, 0])
    frame.add_atom(Atom("H"), [0, 0, 0])

    frame.add_bond(0, 1)
    frame.add_bond(1, 2)
    frame.add_bond(2, 3)

    return frame


class TestSelection(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(Selection("name H").__repr__(), "Selection('name H')")

    def test_copy(self):
        # Just checking that we can call copy.copy on a selction
        selection = Selection("name H")
        copy.copy(selection)

    def test_size(self):
        self.assertEqual(Selection("name H").size, 1)
        self.assertEqual(Selection("pairs: all").size, 2)
        self.assertEqual(Selection("dihedrals: all").size, 4)

    def test_string(self):
        self.assertEqual(Selection("name H").string, "name H")

    def test_evaluate(self):
        frame = testing_frame()

        selection = Selection("name H")
        res = selection.evaluate(frame)
        self.assertEqual(res, [0, 3])

        selection = Selection("bonds: all")
        res = selection.evaluate(frame)

        self.assertIn((0, 1), res)
        self.assertIn((1, 2), res)
        self.assertIn((2, 3), res)

        selection = Selection("angles: all")
        res = selection.evaluate(frame)

        self.assertIn((0, 1, 2), res)
        self.assertIn((1, 2, 3), res)

        selection = Selection("dihedrals: all")
        res = selection.evaluate(frame)

        self.assertEqual([(0, 1, 2, 3)], res)


if __name__ == "__main__":
    unittest.main()
