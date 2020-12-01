# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import warnings

import chemfiles
from chemfiles import Trajectory, ChemfilesError


class RemoveChemfilesWarnings(object):
    def __enter__(self):
        chemfiles.set_warnings_callback(lambda u: None)

    def __exit__(self, *args):
        chemfiles.misc._set_default_warning_callback()


remove_warnings = RemoveChemfilesWarnings()


class TestErrors(unittest.TestCase):
    def test_last_error(self):
        chemfiles.misc._clear_errors()
        self.assertEqual(chemfiles.misc._last_error(), "")

        try:
            with remove_warnings:
                Trajectory("noextention")
        except ChemfilesError:
            pass
        self.assertEqual(
            chemfiles.misc._last_error(),
            "file at 'noextention' does not have an extension, provide a "
            "format name to read it",
        )

        chemfiles.misc._clear_errors()
        self.assertEqual(chemfiles.misc._last_error(), "")


LAST_MESSAGE = ""


class TestWarnings(unittest.TestCase):
    def test_warning(self):
        def callback(message):
            global LAST_MESSAGE
            LAST_MESSAGE = message

        chemfiles.set_warnings_callback(callback)

        try:
            Trajectory("noextention")
        except ChemfilesError:
            pass

        self.assertEqual(
            LAST_MESSAGE,
            "file at 'noextention' does not have an extension, provide a "
            "format name to read it",
        )

        chemfiles.misc._set_default_warning_callback()

    def test_warning_with_exception(self):
        def callback(message):
            global LAST_MESSAGE
            LAST_MESSAGE = message
            raise Exception("test exception in callback")

        chemfiles.set_warnings_callback(callback)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                Trajectory("noextention")
            except ChemfilesError:
                pass

        self.assertEqual(
            LAST_MESSAGE,
            "file at 'noextention' does not have an extension, provide a "
            "format name to read it",
        )

        chemfiles.misc._set_default_warning_callback()


class TestFormatList(unittest.TestCase):
    def test_format_list(self):
        formats = chemfiles.formats_list()

        xyz = formats[-1]
        self.assertEqual(xyz.name, "XYZ")
        self.assertEqual(xyz.description, "XYZ text format")
        self.assertEqual(xyz.extension, ".xyz")

        self.assertEqual(xyz.read, True)
        self.assertEqual(xyz.memory, True)
        self.assertEqual(xyz.atoms, True)
        self.assertEqual(xyz.bonds, False)


if __name__ == "__main__":
    unittest.main()
