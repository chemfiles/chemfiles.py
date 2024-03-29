# Python binding for the chemfiles library

[![Build Status](https://github.com/chemfiles/chemfiles.py/actions/workflows/tests.yml/badge.svg)](https://github.com/chemfiles/chemfiles.py/actions/workflows/tests.yml)
[![Code coverage](http://codecov.io/github/chemfiles/chemfiles.py/coverage.svg?branch=master)](http://codecov.io/github/chemfiles/chemfiles.py?branch=master)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://chemfiles.github.io/chemfiles.py/)

Chemfiles is a library for reading and writing molecular trajectory files. These
files are created by your favorite theoretical chemistry program, and contains
information about atomic or residues names and positions. Chemfiles offers
abstraction on top of these formats, and a consistent interface for loading and
saving data to these files.

This repository contains the Python binding for the chemfiles library. This
binding is created with the ctypes module, calling directly the C interface of
chemfiles, and thus is compatible with Python 2 and 3, and with all versions of
Numpy.

## Installation

You can use your favorite package manager ([`conda`] or [`pip`]) to install
pre-built versions of Chemfiles, that support Linux/Windows/macOS, and Python
2.7 and 3.

```
# Using pip
pip install chemfiles
# Using conda
conda install -c conda-forge chemfiles
```

[`conda`]: http://conda.pydata.org/docs/
[`pip`]: https://docs.python.org/3.5/installing/index.html

### Source compilation

You can install this python module from sources if you have all the
[dependencies] of the C++ chemfiles library installed on your computer.

```bash
# To get the latest development version:
git clone https://github.com/chemfiles/chemfiles.py
cd chemfiles.py
git submodule update --init
# Install development dependencies
pip install -r dev-requirements.txt
# Install chemfiles
pip install .
# Optionally run the test suite
tox
```

[dependencies]: http://chemfiles.readthedocs.org/en/latest/installation.html

## Usage example

Here is a simple usage example for the `chemfiles` module. Please see the
`examples` folder for more examples.

```python
from chemfiles import Trajectory, Frame

trajectory = Trajectory("filename.xyz")
frame = trajectory.read()

print(f"There are {len(frame.atoms)} atoms in the frame")
positions = frame.positions()

# Do awesome things with the positions here !
```

## Bug reports, feature requests

Please report any bug you find and any feature you may want as a [github
issue](https://github.com/chemfiles/chemfiles.py/issues/new).
