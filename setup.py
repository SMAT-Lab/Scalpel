from setuptools import setup, find_packages
setup( 
    name = "Scalpel",
    version = "1.0beta",
    description = "Scalpel: A Python Program Analysis Framework",
    author = "Jiawei Wang and Li Li",
    author_email = "jiawei.wang1@monash.edu, li.li@monash.edu",
    url = "https://www.monash.edu",
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

