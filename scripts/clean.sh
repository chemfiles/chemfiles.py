#!/usr/bin/env bash

set -ex

find . -name "*.pyc" -delete
find . -name "__pycache__" | xargs rm -rf
find . -name ".mypy_cache" | xargs rm -rf

rm -rf .tox
rm -rf build
rm -rf dist
rm -rf MANIFEST
rm -rf .coverage
rm -rf src/chemfiles.egg-info
rm -rf doc/_build

rm -rf src/chemfiles/*.dylib
rm -rf src/chemfiles/*.so
rm -rf src/chemfiles/*.dll
rm -rf src/chemfiles/external.py
