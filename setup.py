# -*- coding=utf-8 -*-
from setuptools import setup
from chemharp import __version__

setup(
    name="chemharp",
    version=__version__,
    author="Guillaume Fraux",
    author_email="luthaf@luthaf.fr",
    description=("A cross-platform library for chemistry files IO"),
    license="MPL-v2.0",
    keywords="chemistry computational cheminformatics files formats",
    url="http://github.com/Luthaf/Chemharp-python",
    packages=['chemharp'],
    long_description='TODO',
    install_requires=["enum34"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
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
)
