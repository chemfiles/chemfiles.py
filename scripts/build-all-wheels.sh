#!/bin/bash

# Build wheel for all the main platforms
#
# This script can only run on OS X, with dockcross installed

set -xe

ROOT=$(cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)
cd $ROOT

if [[ $(uname) != "Darwin" ]]; then
    echo "This script should run from an OSX computer"
    exit 2
fi

rm -rf dist/
./scripts/clean.sh

# make source distribution
python setup.py sdist

# Build for OS X
./scripts/build-wheel.sh macos

# Build for Linux and windows using dockcross
for image in manylinux1-x64 manylinux1-x86 windows-static-x64 windows-static-x86
do
    dockcross -i dockcross/$image ./scripts/build-wheel.sh $image
done

rm dist/numpy-*

twine check dist/chemfiles-*.whl
