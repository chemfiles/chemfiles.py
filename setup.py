# -*- coding=utf-8 -*-
import chemfiles
import sys
from wheel.bdist_wheel import bdist_wheel
from skbuild import setup


class universal_wheel(bdist_wheel):
    # Workaround until https://github.com/pypa/wheel/issues/185 is resolved
    def get_tag(self):
        tag = bdist_wheel.get_tag(self)
        return ('py2.py3', "none") + tag[2:]


with open('requirements.txt', 'r') as fp:
    requirements = list(filter(bool, (line.strip() for line in fp)))
    if sys.hexversion >= 0x03040000:
        requirements = list(filter(lambda r: r != "enum34", requirements))

LONG_DESCRIPTION = """Chemfiles is a library for reading and writing molecular
trajectory files. These files are created by your favorite theoretical chemistry
program, and contains informations about atomic or residues names and positions.
Chemfiles offers abstraction on top of these formats, and a consistent interface
for loading and saving data to these files."""

setup(
    name="chemfiles",
    long_description=LONG_DESCRIPTION,
    version=chemfiles.__version__,
    author="Guillaume Fraux",
    author_email="luthaf@luthaf.fr",
    description="Read and write chemistry trajectory files",
    license="BSD",
    keywords="chemistry computational cheminformatics files formats",
    url="http://github.com/chemfiles/chemfiles.py",
    packages=['chemfiles'],
    zip_safe=False,
    install_requires=requirements,
    setup_requires=["scikit-build"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    cmake_install_dir="chemfiles",
    cmdclass={'bdist_wheel': universal_wheel},
)
