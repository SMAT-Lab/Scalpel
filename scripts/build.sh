#!/usr/bin/env bash
# -*- encoding: utf-8 -*-

set -x

# upgrade pip
python3 -m pip install --upgrade pip

# install PyPA's build
python3 -m pip install --upgrade build

# build dist files including source distribution and built distribution
python3 -m build

# install twine to upload the distribution packages.
python3 -m pip install --upgrade twine

# upload distributions to PyPI
python3 -m twine upload dist/*
