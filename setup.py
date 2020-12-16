# -*- coding=utf-8 -*-
from wheel.bdist_wheel import bdist_wheel
from skbuild import setup

import sys
import os
import re


# Read the version from chemfiles/__init__.py without importing chemfiles
__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', open("chemfiles/__init__.py").read()
).group(1)


class universal_wheel(bdist_wheel):
    # Workaround until https://github.com/pypa/wheel/issues/185 is resolved
    def get_tag(self):
        tag = bdist_wheel.get_tag(self)
        return ("py2.py3", "none") + tag[2:]


install_requires = ["numpy"]
if sys.hexversion < 0x03040000:
    install_requires.append("enum34")


# scikit-build options
cmake_args = []
if sys.platform.startswith("darwin"):
    cmake_args.append("-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9")

if os.getenv("CHFL_PY_INTERNAL_CHEMFILES"):
    cmake_args.append("-DCHFL_PY_INTERNAL_CHEMFILES=ON")


def _get_lib_ext():
    if sys.platform.startswith("win32"):
        ext = ".dll"
    elif sys.platform.startswith("darwin"):
        ext = ".dylib"
    elif sys.platform.startswith("linux"):
        ext = ".so"
    else:
        raise Exception("Unknown operating system: %s" % sys.platform)
    return ext


setup(
    version=__version__,
    install_requires=install_requires,
    cmdclass={"bdist_wheel": universal_wheel},
    cmake_args=cmake_args,
    packages=["chemfiles"],
    package_data={
        "chemfiles": [
            "*" + _get_lib_ext(),
            "bin/*" + _get_lib_ext(),
        ]
    },
    exclude_package_data={
        "chemfiles": [
            "include/*",
        ]
    },
)
