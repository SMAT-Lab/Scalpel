"""
Scalpel: Static Anaysis for Python Programs
==================================
Scalpel is a Python library integrating classical program anaysis algorithms
with tailored features for Python language. It aims to provide simple and efficient solutions to software engineering researchers that are accessible to
everybody and reusable in various contexts.
For more information, please see Scalpel: [The Python Static Analysis Framework](https://github.com/SMAT-Lab/Scalpel)
"""

__all__ = ["cfg", "call_graph", "SSA", "core", "typeinfer", "import_graph", "duc", "rewriter", "file_system"]
__version__ = "1.0dev"

from .util import check_python_version
check_python_version()
