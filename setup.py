# -*- coding=utf-8 -*-
import chemfiles
import sys
from wheel.bdist_wheel import bdist_wheel
from skbuild import setup


class universal_wheel(bdist_wheel):
    # Workaround until https://github.com/pypa/wheel/issues/185 is resolved
    def get_tag(self):
        tag = bdist_wheel.get_tag(self)
        return ("py2.py3", "none") + tag[2:]


with open("requirements.txt", "r") as fd:
    requirements = list(filter(bool, (line.strip() for line in fd)))
    if sys.hexversion >= 0x03040000:
        requirements = list(filter(lambda r: r != "enum34", requirements))


long_description = ""
with open("README.md", "r") as fd:
    for line in fd:
        # remove github badges
        if not line.startswith("[!["):
            long_description += line

setup(
    name="chemfiles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=chemfiles.__version__,
    author="Guillaume Fraux",
    author_email="luthaf@luthaf.fr",
    description="Read and write chemistry trajectory files",
    keywords="chemistry computational cheminformatics files formats",
    url="http://github.com/chemfiles/chemfiles.py",
    packages=["chemfiles"],
    zip_safe=False,
    install_requires=requirements,
    setup_requires=["scikit-build"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    cmake_install_dir="chemfiles",
    cmake_args=['-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9'],
    cmdclass={"bdist_wheel": universal_wheel},
)
