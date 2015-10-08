# -*- coding=utf-8 -*-
import os
import sys
import glob
import shutil
import inspect

from setuptools import setup
from distutils.command.build import build as _build
from setuptools.command.install import install as _install
from subprocess import Popen, PIPE, call

CMAKE_OPTS = [("BUILD_SHARED_LIBS", "ON"), ("BUILD_FRONTEND", "OFF")]

# Get current file even when using execfile
__file__ = inspect.getfile(inspect.currentframe())
CHEMFILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "native")

VERSION = open(os.path.join(CHEMFILES_DIR, "VERSION")).read().strip()
VERSION = VERSION.replace("-", "_")


def check_cmake():
    try:
        cmd = Popen(["cmake"], stdout=PIPE, stderr=PIPE)
        cmd.wait()
    except OSError:
        raise EnvironmentError("CMake is not available!")


def write_version():
    ROOT = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(ROOT, "chemfiles", "_version.py"), "w") as fd:
        fd.write('__version__ = "{}"\n'.format(VERSION))


class BuildCmake(_build):
    '''Build binary package using cmake'''

    def run(self):
        check_cmake()
        write_version()
        BUILD_DIR = os.path.join(os.path.dirname(self.build_lib), "native")
        try:
            os.makedirs(BUILD_DIR)
        except OSError:
            pass
        cwd = os.getcwd()
        os.chdir(BUILD_DIR)

        configure = ["cmake", CHEMFILES_DIR]
        cmake_opts = ['-D' + '='.join(opt) for opt in CMAKE_OPTS]
        configure.extend(cmake_opts)
        if call(configure) != 0:
            raise EnvironmentError("Error in CMake configuration")

        build = ["cmake", "--build", "."]
        if call(build) != 0:
            raise EnvironmentError("Error while building chemfiles")
        os.chdir(cwd)
        # can't use super() here because _build is an old style class in 2.7
        _build.run(self)

        CHEMFILES_PATH = os.path.join(self.build_lib, "chemfiles")
        for path in glob.iglob(os.path.join(BUILD_DIR, "*chemfiles*")):
            filename = os.path.basename(path)
            dest = os.path.join(CHEMFILES_PATH, filename)
            print("copying {} -> {}".format(path, dest))
            shutil.copy(path, dest)


class InstallCmake(_install):
    '''Install binary package built with cmake by calling build'''
    def run(self):
        self.run_command('build')
        _install.run(self)


LONG_DESCRIPTION = """Chemfiles is a library for reading and writing molecular
trajectory files. These files are created by your favorite theoretical
chemistry program, and contains informations about atomic or residues names
and positions. Chemfiles offers abstraction on top of these formats, and a
consistent interface for loading and saving data to these files."""

options = {
    "name": "chemfiles",
    "version": VERSION,
    "author": "Guillaume Fraux",
    "author_email": "luthaf@luthaf.fr",
    "description": ("An efficient library for chemistry files IO"),
    "license": "MPL-v2.0",
    "keywords": "chemistry computational cheminformatics files formats",
    "url": "http://github.com/chemfiles/chemfiles.py",
    "packages": ['chemfiles'],
    "long_description": LONG_DESCRIPTION,
    "install_requires": ["numpy"],
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    "cmdclass": {'build': BuildCmake, 'install': InstallCmake}
}

if sys.hexversion < 0x03040000:
    options["install_requires"].append("enum34")

setup(**options)
