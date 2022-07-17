from setuptools import setup, find_packages
setup( 
    name = "Scalpel",
    version = "1.0beta",
    description = "The Python Static Analysis Framework",
    author = "Jiawei Wang and Li Li",
    url = "https://github.com/SMAT-Lab/Scalpel",
    packages= find_packages(include=['scalpel', 'scalpel.*']),
    install_requires = [
        'astor~=0.8.1',
        'graphviz~=0.17',
        'networkx',
        'astunparse~=1.6.3',
        'typed-ast',
        'typeshed-client',
        'regex',
        'setuptools',
        'dataclasses',
        'pycg',
    ]
    )

