"""
Utilities for type inference module
"""

import re
import ast
import sys
import builtins
from copy import deepcopy
from collections import deque
from typing import Dict, Union, List


def get_func_calls_type(tree):
    node = deepcopy(tree)
    transformer = TypeInferCallTransformer()
    transformer.visit(node)
    return transformer.call_names


class TypeInferCallTransformer(ast.NodeTransformer):
    """
    A NodeTransformer class for getting function call information
    """
    def __init__(self):
        self.call_names = []

    # def visit_FunctionDef(self, node):
    #    node.decorator_list = []
    #    self.generic_visit(node)
    #    return node

    def visit_Attribute(self, node):
        #        self.generic_visit(node.value)
        return node

    def visit_Call(self, node):

        tmp_fun_node = deepcopy(node)
        tmp_fun_node.args = []
        tmp_fun_node.keywords = []

        callvisitor = FuncCallVisitor()
        callvisitor.visit(tmp_fun_node)

        self.call_names += [callvisitor.name]
        for arg in node.args:
            self.generic_visit(arg)

        for kw in node.keywords:
            self.generic_visit(kw)
        self.generic_visit(tmp_fun_node)

        return node


class FuncCallVisitor(ast.NodeVisitor):
    """
    A NodeVisitor class for getting function call information
    """
    def __init__(self):
        self._name = deque()
        self.call_names = []

    def clear(self):
        self._name = deque()
        self.call_names = []

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):

        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError as e:
            self.generic_visit(node)

    def visit_Call(self, node):
        node.args = []
        node.keywords = []
        self.generic_visit(node)
        return node


def get_built_in_types() -> Dict:
    """
    Gets Python built in types

    :return: Python built in types in a dictionary
    """
    builtin_types = [getattr(builtins, d).__name__ for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
    builtin_types_dict = {}
    for b in builtin_types:
        builtin_types_dict[b.lower()] = b
    return builtin_types_dict


def get_type(node, imports=None) -> str:
    """
    Get the type of a node
    Args:
        node: The node to get the type of
        imports: Dictionary of known imported types
    Returns:
        The type of the node
    """

    # TODO: Implement consistent list types where required
    if node is None:
        return any.__name__
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
    elif isinstance(node, ast.List) or isinstance(node, ast.Tuple):
        value_type = check_consistent_list_types(node.elts)
        return f"{type(node).__name__}[{value_type}]"
    elif isinstance(node, ast.Subscript):
        return "subscript"
    elif isinstance(node, ast.Dict):
        key_type = check_consistent_list_types(node.keys)
        value_type = check_consistent_list_types(node.values)
        return f"Dict[{key_type}, {value_type}]"
    elif isinstance(node, ast.Set):
        return "set"
    elif isinstance(node, ast.SetComp):
        return "set"
    elif isinstance(node, ast.Str):
        return "str"
    elif isinstance(node, ast.JoinedStr):
        return "str"
    elif isinstance(node, ast.Constant):
        return get_type(node.value)
    elif isinstance(node, ast.NameConstant):
        return any.__name__
    elif isinstance(node, ast.Lambda):
        return "lambda"
    elif isinstance(node, ast.DictComp):
        return "dict"
    elif isinstance(node, ast.ListComp):
        return "list"
    elif isinstance(node, ast.GeneratorExp):
        return "generator"
    elif isinstance(node, ast.Call):
        func_name = get_func_calls_type(node)
        func_name = func_name[0]
        # Check to see if it is an imported callable
        if imports is not None:
            imported_type = imports.get(func_name)
            if imported_type:
                return imported_type
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
                return any.__name__
            elif node.func.id in ["iter"]:
                return "iterator"
            elif node.func.id in ["isinstance"]:
                return any.__name__
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
    elif isinstance(node, bool):
        return bool.__name__
    else:
        return "unknown"


def check_consistent_list_types(values) -> str:
    """
    Checks a list of values to see if they have a constant type
    """

    if len(values) == 0:
        # Nothing in list yet so return any
        return any.__name__
    first_type = type(values[0])
    assignment_type = any.__name__
    if not first_type == ast.Constant:
        builtin_types_dict = get_built_in_types()
        builtin_first_type = builtin_types_dict.get(first_type.__name__.lower())
        # Not an AST constant so we can just compare AST types
        for n in values[1:len(values)]:
            # Compare type to first items type
            if not isinstance(n, first_type):
                # No constant type, assign any
                assignment_type = any.__name__
                break
            else:
                assignment_type = builtin_first_type
    else:
        # We have an AST constant so we will need to compare their types
        first_constant_type = type(values[0].value)
        assignment_type = first_constant_type.__name__
        for n in values[1:len(values)]:
            # Compare type to first items type
            if not isinstance(n, ast.Constant):
                # Not a constant type, assign any
                assignment_type = any.__name__
                break
            else:
                if not isinstance(n.value, first_constant_type):
                    assignment_type = any.__name__
                    break
    return assignment_type


def is_camel_case(s: str) -> bool:
    """
    Determines whether a string is written in camel case

    Args:
        s: The string to check
    Returns:
        True if the string is camel case, False otherwise
    """
    pattern = '([A-Z][a-z]*)+'
    if re.search(pattern, s):
        return True
    return False


def parse_module(m_ast):
    """
    Get the function, class and import nodes for a module
    Args:
        m_ast: The AST tree to get the nodes for
    Returns:
        Tuple containing list of function nodes, list of class nodes and list of import nodes
    """
    fun_nodes = []
    class_nodes = []
    import_nodes = []

    for node in ast.walk(m_ast):
        if isinstance(node, ast.FunctionDef):
            fun_nodes += [node]
        if isinstance(node, ast.ClassDef):
            class_nodes += [node]
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


def is_imported_fun(func_name: str, import_dict: dict) -> Union[str, None]:
    """
    Determines whether a function is imported from another library

    Args:
        func_name: The name of the function to check
        import_dict: Dictionary of import modules
    Returns:
        The module that the function was import from or None if it was not imported
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


def generate_ast(source: str):
    """
    Generates ast from the source string
    """
    try:
        if sys.version_info >= (3,8):
            tree = ast.parse(source, mode='exec', type_comments=True)
        elif sys.version_info >= (3,5) and sys.version_info < (3,8):
            tree = ast.parse(source, mode='exec')
        else:
            raise Exception("Must use Python 3.5+ ")
        #tree = ast.parse(source, mode='exec')
        return tree
    except Exception as e:
        print(e)
        return None


def get_function_comment(source: str) -> str:
    """
    Get the function comment header for function source code
    Args:
        source: The function source code to check
    Returns:
        The function header comment
    """
    matches = re.findall(r"\'(.+?)\'", source)
    comment = ""
    if len(matches) > 0:
        comment = matches[0]
    return comment


def is_done(t_vals: List[str]) -> bool:
    """
    Determines whether a list of type values is in a finished state
    Args:
        t_vals: List of type values to check
    Returns:
        True if in a finished state, False otherwise
    """
    return all(x not in ['ID', 'call', 'unknown', 'input', '3call'] for x in t_vals)


def find_class_by_attr(module_records, attrs):
    if len(attrs) < 5:
        return None
    class_names = [item.split('.')[0] for item in module_records if len(item.split('.')) == 2]
    class_names = list(set(class_names))
    for c_name in class_names:
        if all([(c_name + '.' + x) in module_records for x in attrs]):
            return c_name

    return None


def get_attr_name(node):
    if isinstance(node, ast.Call):
        return get_attr_name(node.func)
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return get_attr_name(node.value) + "." + node.attr
    elif isinstance(node, ast.Subscript):
        return ""
    return ""


def resolve_name(node: any) -> Union[str, None]:
    """
    Resolve the string name of an AST node
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        # TODO: Attributes will have to be resolved to their classes, due to classes having same attribute names
        return node.attr
    elif isinstance(node, ast.Call):
        return node.func.id
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        return None
