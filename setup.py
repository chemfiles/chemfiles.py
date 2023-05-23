import os
import re
import site
import subprocess
import sys

from setuptools import Extension, setup
from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
from wheel.bdist_wheel import bdist_wheel

# workaround https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

# Read the version from chemfiles/__init__.py without importing chemfiles
ROOT = os.path.realpath(os.path.dirname(__file__))
__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', open("src/chemfiles/__init__.py").read()
).group(1)


class universal_wheel(bdist_wheel):
    # Workaround until https://github.com/pypa/wheel/issues/185 is resolved
    def get_tag(self):
        tag = bdist_wheel.get_tag(self)
        return ("py2.py3", "none") + tag[2:]


class cmake_configure(build_py):
    """configure cmake to build chemfiles and generate external.py"""

    def run(self):
        source_dir = ROOT
        build_dir = os.path.join(ROOT, "build", "cmake-build")
        install_dir = os.path.join(os.path.realpath(self.build_lib))

        try:
            os.makedirs(build_dir)
        except OSError:
            pass

        cmake_options = [
            "-GNinja",
            f"-DCMAKE_INSTALL_PREFIX={install_dir}",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DBUILD_SHARED_LIBS=ON",
        ]

        if sys.platform.startswith("darwin"):
            cmake_options.append("-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9")

        # ARCHFLAGS is used by cibuildwheel to pass the requested arch to the
        # compilers
        ARCHFLAGS = os.environ.get("ARCHFLAGS")
        if ARCHFLAGS is not None:
            cmake_options.append(f"-DCMAKE_C_FLAGS={ARCHFLAGS}")
            cmake_options.append(f"-DCMAKE_CXX_FLAGS={ARCHFLAGS}")

        if os.getenv("CHFL_PY_INTERNAL_CHEMFILES"):
            cmake_options.append("-DCHFL_PY_INTERNAL_CHEMFILES=ON")

        subprocess.run(
            ["cmake", source_dir, *cmake_options],
            cwd=build_dir,
            check=True,
        )

        return super().run()


class cmake_build(build_ext):
    """build and install chemfiles with cmake"""

    def run(self):
        build_dir = os.path.join(ROOT, "build", "cmake-build")

        subprocess.run(
            ["cmake", "--build", build_dir],
            check=True,
        )

        subprocess.run(
            ["cmake", "--install", build_dir, "--strip"],
            check=True,
        )


class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg

    Prevents setup.py install performing setuptools' default easy_install,
    which it should never ever do.
    """

    def run(self):
        sys.exit(
            "Aborting implicit building of eggs. "
            + "Use `pip install .` or `python setup.py bdist_wheel && pip "
            + "uninstall chemfiles -y && pip install dist/chemfiles-*.whl` "
            + "to install from source."
        )


setup(
    version=__version__,
    ext_modules=[
        # only declare the extension, it is built & copied as required by cmake
        # in the build_ext command
        Extension(name="chemfiles", sources=[]),
    ],
    cmdclass={
        "build_py": cmake_configure,
        "build_ext": cmake_build,
        "bdist_wheel": universal_wheel,
        "bdist_egg": bdist_egg if "bdist_egg" in sys.argv else bdist_egg_disabled,
    },
    exclude_package_data={
        "chemfiles": [
            "include/*",
        ]
    },
)
