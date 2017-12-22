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
mkdir -p dist

# make source distribution
python setup.py sdist

# Build for OS X
./scripts/build-wheel.sh macos

# Build for Linux
for image in manylinux-x64 manylinux-x86
do
    dockcross -i dockcross/$image ./scripts/build-wheel.sh $image
done

docker build scripts/chemfiles-w64 --tag chemfiles-w64:latest
docker build scripts/chemfiles-w32 --tag chemfiles-w32:latest

# Build for Windows
for image in chemfiles-w64 chemfiles-w32
do
    dockcross -i $image ./scripts/build-wheel.sh $image
done
