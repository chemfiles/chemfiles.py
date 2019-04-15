#!/usr/bin/env bash

set -ex

find . -name "*.pyc" -delete

rm -rf .tox
rm -rf _skbuild
rm -rf dist
rm -rf chemfiles.egg-info
