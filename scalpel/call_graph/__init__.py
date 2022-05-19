"""
A call graph depicts calling relationships between subroutines in a computer program. 
It is an essential component in most static analysis and can be leveraged to build more sophisicated applications such as profiling, vunerability propagation and refactoring. 

Please note scalpel.pycg module is a wrapper of [PyCG](https://pypi.org/project/pycg/). 
It aims to construct the call graphs for given Python projects. 

The basic node can be either a function, a class or a module. 
The edges represent calling relationships between program nodes.
"""

