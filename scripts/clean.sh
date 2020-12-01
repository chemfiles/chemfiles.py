#!/usr/bin/env bash

set -ex

find . -name "*.pyc" -delete
find . -name "__pycache__" | xargs rm -rf

rm -rf .tox
rm -rf _skbuild
rm -rf dist
rm -rf MANIFEST
rm -rf chemfiles.egg-info

rm -rf chemfiles/*.dylib
rm -rf chemfiles/*.so
rm -rf chemfiles/*.dll
rm -rf chemfiles/external.py
