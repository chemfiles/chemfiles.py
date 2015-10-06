# Python binding for the Chemharp library

This repository contains the Python binding for the Chemharp library. This binding is
created with the ctypes module, calling directly the C interface of Chemharp, and thus
is compatible with Python 2 and 3, and with all versions of Numpy.

## Installation

### Using Conda

Using the [`conda`](http://conda.pydata.org/docs/) package manager is the preferred way to
install the chemharp Python module.

```
conda install -c https://conda.anaconda.org/luthaf chemharp
```

### Source compilation

You can install this python module from sources if you have all the
[dependencies](http://chemharp.readthedocs.org/en/latest/installation.html)  of theC++
library installed on your computer.

```bash
# To get the latest developement version:
pip install https://github.com/Luthaf/Chemharp.py/archive/master.zip
```

## Usage example

Here is a simple usage example for the `chemharp` module. Please see the `examples` folder
for other examples.

```python
from chemharp import Trajectory, Frame

trajectory = Trajectory("filename.xyz")
frame = trajectory.read()

print("There are {} atoms in the frame".format(frame.natoms()))
positions = frame.positions()

# Do awesome things with the positions here !
```

## Bug reports, feature requests

Please report any bug you find and any feature you may want as a [github issue](https://github.com/Luthaf/Chemharp.py/issues/new).
