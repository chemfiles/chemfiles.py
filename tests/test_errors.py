# -*- coding=utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import unittest
import os

from chemfiles import logging, Trajectory
from chemfiles.logging import LogLevel


class TestLogging(unittest.TestCase):
    def test_level(self):
        self.assertEqual(logging.log_level(), LogLevel.WARNING)
        logging.set_log_level(LogLevel.DEBUG)
        self.assertEqual(logging.log_level(), LogLevel.DEBUG)
        logging.set_log_level(LogLevel.ERROR)

    def test_redirect(self):
        logging.log_to_file("test.log")
        self.assertTrue(os.path.isfile("test.log"))
        logging.log_to_stderr()
        os.unlink("test.log")

    def test_callback(self):
        filename = "tmp.mylog"

        def callback(level, message):
            with open(filename, "w") as fd:
                fd.write("{}: {}".format(repr(level), message))

        logging.log_callback(callback)
        try:
            # Just generating a log message
            Trajectory("nothere")
        except:
            pass

        logging.log_to_stderr()

        with open(filename) as fd:
            content = fd.read()
            self.assertEqual(
                content,
                '<LogLevel.ERROR: 0>:' +
                ' Can not find a format associated with the "" extension.'
            )
        os.unlink(filename)


if __name__ == '__main__':
    unittest.main()
