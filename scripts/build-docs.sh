#!/bin/bash -xe

# Install doc dependencies
cd $TRAVIS_BUILD_DIR
pip install -r doc/requirements.txt

# Get previous documentation
git clone https://github.com/$TRAVIS_REPO_SLUG --branch gh-pages gh-pages
rm -rf gh-pages/.git

# Build documentation
cd $TRAVIS_BUILD_DIR/build
cmake -DCHFL_PY_BUILD_DOCUMENTATION=ON .
make python_doc_html
rm -rf doc/html/_static/bootswatch-* doc/html/_static/bootstrap-2.3.2

cd ../gh-pages

# Copy the right directory
if [[ "$TRAVIS_TAG" != "" ]]; then
    mv ../build/doc/html/ $TRAVIS_TAG
else
    rm -rf latest
    mv ../build/doc/html/ latest
fi
