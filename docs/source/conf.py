# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

import os
import pathlib
import subprocess


project = 'Scalpel'
copyright = '2022, Jiawei Wang and Li Li'
author = 'Jiawei Wang and Li Li'

# The full version, including alpha/beta/rc tags
release = '1.0beta'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser', 
    'sphinx.ext.doctest',
    'sphinx_rtd_theme',
    'sphinxcontrib.spelling',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'pydoctor.sphinx_ext.build_apidocs',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# interpshinx

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# API docs configuration

_project_root = pathlib.Path(__file__).parent.parent.parent

# -- Extension configuration ----------------------------------------------
_git_reference = subprocess.run(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    text=True,
    encoding="utf8",
    capture_output=True,
    check=True,
).stdout.strip()

# See Read The Docs environment variables
# https://docs.readthedocs.io/en/stable/builds.html#build-environment
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

# Try to find URL fragment for the GitHub source page based on current
# branch or tag.

if _git_reference == "HEAD":
    # It looks like the branch has no name.
    # Fallback to commit ID.
    _git_reference = subprocess.getoutput("git rev-parse HEAD").strip()

pydoctor_args = [
    '--project-name=Scalpel',
    f'--project-version={release}',
    '--project-url=../',
    '--docformat=google', 
    '--theme=readthedocs',
    '--intersphinx=https://docs.python.org/3/objects.inv',
    f'--html-viewsource-base=https://github.com/SMAT-Lab/Scalpel/{_git_reference}/',
    '--html-output={outdir}/api',
    f'--project-base-dir={_project_root}',
    f'{_project_root}/scalpel'
    ]

if on_rtd:
    pydoctor_url_path = '/en/{rtd_version}/api/'
else:
    pydoctor_url_path = '/api/'
