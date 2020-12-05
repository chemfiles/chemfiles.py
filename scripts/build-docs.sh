#!/bin/bash -xe

# Install doc dependencies
pip install --user -r doc/requirements.txt
export PATH=$PATH:$HOME/.local/bin

# Get previous documentation
git clone https://github.com/$GITHUB_REPOSITORY --branch gh-pages gh-pages
rm -rf gh-pages/.git

# Build documentation
cd doc
make html
rm -rf _build/html/.doctrees/ _build/html/.buildinfo
rm -rf _build/html/_static/bootswatch-2.3.2/ _build/html/_static/bootstrap-2.3.2/
shopt -s extglob
cd _build/html/_static/bootswatch-* && rm -rf !(flatly) && cd -
cd ..

REF_KIND=$(echo $GITHUB_REF | cut -d / -f2)
if [[ "$REF_KIND" == "tags" ]]; then
    TAG=${GITHUB_REF#refs/tags/}
    mv doc/_build/html/ gh-pages/$TAG
else
    rm -rf gh-pages/latest
    mv doc/_build/html/ gh-pages/latest
fi
