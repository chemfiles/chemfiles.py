# Python binding for the chemfiles library

[![Build Status](https://travis-ci.org/chemfiles/chemfiles.py.svg?branch=master)](https://travis-ci.org/chemfiles/chemfiles.py)
[![Code coverage](http://codecov.io/github/chemfiles/chemfiles.py/coverage.svg?branch=master)](http://codecov.io/github/chemfiles/chemfiles.py?branch=master)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://chemfiles.github.io/chemfiles.py/)


This repository contains the Python binding for the chemfiles library. This
binding is created with the ctypes module, calling directly the C interface of
chemfiles, and thus is compatible with Python 2 and 3, and with all versions of
Numpy.

## Installation

### Using Conda

Using the [`conda`](http://conda.pydata.org/docs/) package manager is the
preferred way to install the chemfiles Python module.

```
conda install -c conda-forge chemfiles
```

### Source compilation

You can install this python module from sources if you have all the
[dependencies][installation] of the C++ chemfiles library installed on your
computer.

```bash
# To get the latest developement version:
git clone https://github.com/chemfiles/chemfiles.py
cd chemfiles.py
git submodule update --init
mkdir build
cd build
cmake .. <options>  # see below for configuration options.
make
# Optionally
make test
make install
```

You can use the same [configuration options][installation] as the C++ chemfiles
library. Additionally, you may also want to specify which python interpreter and
installation to use with `-DPYTHON_EXECUTABLE=/full/path/to/python`, and where
to install the code with `-DCMAKE_INSTALL_PREFIX=<PREFIX>`. The C++ library will
be installed to `PREFIX/lib/`; and the python code will be installed in
`PREFIX/lib/python<x.y>/site-packages/`.

[installation]: http://chemfiles.readthedocs.org/en/latest/installation.html

## Usage example

Here is a simple usage example for the `chemfiles` module. Please see the
`examples` folder for other examples.

```python
from chemfiles import Trajectory, Frame

trajectory = Trajectory("filename.xyz")
frame = trajectory.read()

print("There are {} atoms in the frame".format(frame.natoms()))
positions = frame.positions()

# Do awesome things with the positions here !
```

## Bug reports, feature requests

Please report any bug you find and any feature you may want as a [github
issue](https://github.com/chemfiles/chemfiles.py/issues/new).
