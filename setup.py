from setuptools import setup, find_packages
setup( 
    name = "python-scalpel",
    version = "1.0beta",
    description = "Scalpel: The Python Program Analysis Framework",
    author = "Jiawei Wang and Li Li and Haowei Quan",
    author_email = "jiawei.wang1@monash.edu, li.li@monash.edu, haowei.quan@monash.edu",
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
        ],
    extras_require = {
        'docs':
            [
            'sphinx', 
            'myst_parser', 
            'sphinx_rtd_theme', 
            'sphinxcontrib-spelling', 
            'pydoctor', 
            ]
        },
    )

