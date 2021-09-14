"""
Tomas Bolger 2021
Python 3.9
Utilities for type inference module
"""
import re
import ast
import builtins
from typing import Dict, Union

from scalpel.core.func_call_visitor import get_func_calls


def get_built_in_types() -> Dict:
    """
    Returns the builtin types for Python
    """
    builtin_types = [getattr(builtins, d).__name__ for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
    builtin_types_dict = {}
    for b in builtin_types:
        builtin_types_dict[b.lower()] = b
    return builtin_types_dict


def get_type(node) -> Union[str, None]:
    if node is None:
        return None
    elif isinstance(node, str) and node[0:3] == "org":
        return node[4:]
    elif isinstance(node, ast.BoolOp):
        return "bool"
    elif isinstance(node, ast.cmpop):
        return "bool"
    elif isinstance(node, ast.Compare):
        return "bool"
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return "bool"
    elif isinstance(node, ast.BinOp):
        if isinstance(node.op, (ast.Div, ast.Mult)):
            return "float"
        elif isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Constant) and isinstance(node.left, ast.Str):
            return "str"
        elif isinstance(node.op, ast.Mod) and isinstance(node.left, ast.Name) and isinstance(node.right, ast.Dict):
            return "str"
        elif isinstance(node.op, ast.Add):
            if isinstance(node.left, (ast.Constant, ast.Num, ast.List, ast.ListComp,
                                      ast.Set, ast.SetComp, ast.Dict, ast.DictComp)):
                return get_type(node.left)

            if isinstance(node.right, (ast.Constant, ast.Num, ast.List, ast.ListComp,
                                       ast.Set, ast.SetComp, ast.Dict, ast.DictComp)):
                return get_type(node.right)
    if isinstance(node, ast.Name):
        if node.id == 'self':
            return "self"
        return 'ID'
    if isinstance(node, ast.Num):
        if isinstance(node.n, int):
            return "int"
        elif isinstance(node.n, float):
            return "float"
        return "num"
    elif isinstance(node, ast.List):
        return "list"
    elif isinstance(node, ast.Subscript):
        return "subscript"
    elif isinstance(node, ast.Tuple):
        return "tuple"
    elif isinstance(node, ast.Dict):
        return "dict"
    elif isinstance(node, ast.Set):
        return "set"
    elif isinstance(node, ast.SetComp):
        return "set"
    elif isinstance(node, ast.Str):
        return "str"
    elif isinstance(node, ast.JoinedStr):
        return "str"
    elif isinstance(node, ast.NameConstant):
        return "NC"
    elif isinstance(node, ast.Constant):
        return get_type(node.value)
    elif isinstance(node, ast.Lambda):
        return "lambda"
    elif isinstance(node, ast.DictComp):
        return "dict"
    elif isinstance(node, ast.ListComp):
        return "list"
    elif isinstance(node, ast.GeneratorExp):
        return "generator"
    elif isinstance(node, ast.Call):
        func_name = get_func_calls(node)
        func_name = func_name[0]
        if isinstance(node.func, ast.Name):
            if node.func.id == "dict":
                return "dict"
            elif node.func.id == "list":
                return "list"
            elif node.func.id == "tuple":
                return "tuple"
            elif node.func.id == "set":
                return "set"
            elif node.func.id == "str":
                return "str"
            elif node.func.id in ["id", "sum", "len", "int", "float", "ceil", "floor", "max", "min"]:
                return "num"
            elif node.func.id in ["all", "any", "assert", "bool"]:
                return "NC"
            elif node.func.id in ["iter"]:
                return "iterator"
            elif node.func.id in ["isinstance"]:
                return "NC"
            elif node.func.id in ['bytes']:
                return "bytes"
            elif is_camel_case(func_name):
                return func_name
            else:
                return "call"
        elif is_camel_case(func_name.split(".")[-1]):
            return func_name
        elif func_name in ['join', 'format']:
            return "str"
        else:
            return "call"
    elif isinstance(node, ast.Attribute):
        return "attr"
    else:
        return "unknown"


def is_camel_case(s: str) -> bool:
    """
    Determines whether a string is written in camel case
    """
    pattern = '([A-Z][a-z]*)+'
    if re.search(pattern, s):
        return True
    return False


def parse_module(m_ast):
    fun_nodes = []
    class_nodes = []
    import_nodes = []

    for node in m_ast.body:
        if isinstance(node, ast.FunctionDef):
            fun_nodes += [node]
        if isinstance(node, ast.ClassDef):
            class_nodes += [node]
    for node in ast.walk(m_ast):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            import_nodes += [node]

    return fun_nodes, class_nodes, import_nodes


def get_api_ref_id(import_nodes):
    id2fullname = {}  # key is the imported module while the value is the prefix
    for node in import_nodes:
        if isinstance(node, ast.Import):
            items = [nn.__dict__ for nn in node.names]
            for d in items:
                if d['asname'] is None:  # alias name not found, use its imported name
                    id2fullname[d['name']] = d['name']
                else:
                    id2fullname[d['asname']] = d['name']  # otherwise , use alias name
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            # for import from statements
            # module names are the head of a API name
            items = [nn.__dict__ for nn in node.names]
            for d in items:
                if d['asname'] is None:  # alias name not found
                    id2fullname[d['name']] = node.module + '.' + d['name']
                else:
                    id2fullname[d['asname']] = node.module + '.' + d['name']
    return id2fullname


def is_imported_fun(func_name, import_dict):
    """
    Determines whether a function is imported from another library
    """
    name_parts = func_name.split('.')
    if name_parts[0] in import_dict:
        return import_dict[name_parts[0]]
    return None


def rename_from_name(from_where, from_name, fun_name):
    if from_where == 'self':
        class_name = fun_name.split('.')[0]
        from_name = class_name + "." + ".".join(from_name.split('.')[1:])
        return from_name
    elif from_where == 'local' or from_where == 'base':
        return from_name


def is_valid_call_link(t_vals):
    return all(x not in ['ID', 'call', 'unknown'] for x in t_vals)
