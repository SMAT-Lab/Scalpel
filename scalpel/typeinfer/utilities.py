"""
Tomas Bolger 2021
Python 3.9
Utilities for type inference module
"""
import ast
import builtins
from typing import Dict


def get_built_in_types() -> Dict:
    builtin_types = [getattr(builtins, d).__name__ for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
    builtin_types_dict = {}
    for b in builtin_types:
        builtin_types_dict[b.lower()] = b
    return builtin_types_dict


