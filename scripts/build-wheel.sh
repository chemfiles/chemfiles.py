#!/bin/bash

# Build a wheel for the current platform

# This is not intended to be run directly by users, but rather in
# conjonction with dockcross to build wheels for all major platforms

set -xe

export CHFL_PY_INTERNAL_CHEMFILES=1

clean_build() {
    # this can not use clean.sh because we do not want to remove the dist folder
    find . -name "*.pyc" -delete
    find . -name "__pycache__" | xargs rm -rf
    find . -name ".mypy_cache" | xargs rm -rf

    rm -rf .tox
    rm -rf build
    rm -rf MANIFEST
    rm -rf .coverage
    rm -rf src/chemfiles.egg-info
    rm -rf doc/_build

    rm -rf chemfiles/*.dylib
    rm -rf chemfiles/*.so
    rm -rf chemfiles/*.dll
    rm -rf chemfiles/external.py
}

IMAGE=$1

if [[ "$IMAGE" == "" ]]; then
    exit 1
fi

if [[ "$IMAGE" == "macos" ]]; then
    clean_build
    export MACOSX_DEPLOYMENT_TARGET=10.9
    python -m pip wheel dist/*.tar.gz -w dist
    exit 0
fi

clean_build

if [[ "$IMAGE" == "manylinux2014-x64" ]]; then
    WHEELS=/tmp/wheels
    /opt/python/cp38-cp38/bin/python -m pip wheel dist/*.tar.gz -w ${WHEELS} --verbose
    # Make sure wheels get the manylinux tag
    auditwheel repair -w ${WHEELS} ${WHEELS}/chemfiles-*.whl
    mv -f ${WHEELS}/chemfiles-*manylinux*.whl dist
fi

if [[ "$IMAGE" == "windows-static-x64" || "$IMAGE" == "windows-static-x86" ]]; then
    function sudo {
        gosu root "$@"
    }

    sudo apt update
    sudo apt install -y python3-pip
    python3 -m pip install --upgrade pip wheel setuptools
    python3 -m pip install cmake ninja

    if [[ "$IMAGE" == "windows-static-x64" ]]; then
        python3 setup.py bdist_wheel --plat-name win_amd64
    fi

    if [[ "$IMAGE" == "windows-static-x86" ]]; then
        python3 setup.py bdist_wheel --plat-name win32
    fi
fi
