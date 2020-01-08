#!/bin/bash

# Build a wheel for the current platform

# This is not intended to be run directly by users, but rather in
# conjonction with dockcross to build wheels for all major platforms

set -xe

clean_build() {
    rm -rf _skbuild/ chemfiles.egg-info
    rm -rf chemfiles/lib/ chemfiles/include/ chemfiles/external.py chemfiles/*.pyc
}

IMAGE=$1

if [[ "$IMAGE" == "" ]]; then
    exit 1
fi

if [[ "$IMAGE" == "macos" ]]; then
    clean_build
    export MACOSX_DEPLOYMENT_TARGET=10.9
    python setup.py bdist_wheel --plat-name macosx-10.9-x86_64
    exit 0
fi

# Switch to root and proceed
if [ $UID -ne 0 ]; then
  exec sudo su root "$0" "$@"
fi

clean_build

WHEELS=/tmp/wheels
export PATH=/opt/python/cp27-cp27m/bin/:$PATH
pip install --user -r dev-requirements.txt

if [[ "$IMAGE" == "manylinux-x64" || "$IMAGE" == "manylinux-x86" ]]; then
    pip wheel . -w ${WHEELS}
    # Make sure wheels get the manylinux tag
    auditwheel repair -w ${WHEELS} ${WHEELS}/chemfiles-*.whl
    mv -f ${WHEELS}/chemfiles-*manylinux*.whl dist
fi

if [[ "$IMAGE" == "chemfiles-w64" ]]; then
    python setup.py bdist_wheel --plat-name win_amd64
fi

if [[ "$IMAGE" == "chemfiles-w32" ]]; then
    python setup.py bdist_wheel --plat-name win32
fi
