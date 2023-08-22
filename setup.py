# Principles from: https://blog.miguelgrinberg.com/post/the-package-dependency-blues
from setuptools import find_packages, setup

setup(
    name="scalpel",
    version="1.0beta",
    description="Scalpel: The Python Program Analysis Framework",
    url="https://github.com/SMAT-Lab/Scalpel",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "astor~=0.8.1",
        "graphviz~=0.17",
        "networkx",
        "astunparse~=1.6.3",
        "typed-ast~=1.5.4",
        "typeshed-client~=2.2.0",
        "regex",
        "setuptools",
        "dataclasses",
        "pycg~=0.0.6",
    ],
    extras_require={
        "docs": [
            "sphinx",
            "myst_parser",
            "sphinx_rtd_theme",
            "sphinxcontrib-spelling",
            "pydoctor",
        ]
    },
)
