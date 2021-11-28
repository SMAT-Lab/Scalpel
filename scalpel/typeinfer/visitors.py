"""
Node visitors used for Type Inference
"""

import ast
from copy import deepcopy
from collections import deque


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
        except AttributeError:
            self.generic_visit(node)

    def visit_Call(self, node):
        node.args = []
        node.keywords = []
        self.generic_visit(node)
        return node


class TypeInferCallTransformer(ast.NodeTransformer):
    """
    A NodeTransformer class for getting function call information
    """
    def __init__(self):
        self.call_names = []

    def visit_Attribute(self, node):
        return node

    def visit_Call(self, node):
        tmp_fun_node = deepcopy(node)
        tmp_fun_node.args = []
        tmp_fun_node.keywords = []

        call_visitor = FuncCallVisitor()
        call_visitor.visit(tmp_fun_node)

        self.call_names += [call_visitor.name]
        for arg in node.args:
            self.generic_visit(arg)

        for kw in node.keywords:
            self.generic_visit(kw)
        self.generic_visit(tmp_fun_node)

        return node


def get_args(node):
    """
    Get the argument types of the node
    Args:
        node: the node being checked
    """
    arg_type = []
    for arg in node.args:
        if isinstance(arg, ast.Name):
            arg_type.append(arg.id)
        elif isinstance(arg, ast.Num):
            arg_type.append("Num")
        elif isinstance(arg, ast.List):
            arg_type.append("List")
        elif isinstance(arg, ast.ListComp):
            arg_type.append("List")
        elif isinstance(arg, ast.Tuple):
            arg_type.append("Tuple")
        elif isinstance(arg, ast.Dict):
            arg_type.append("Dict")
        elif isinstance(arg, ast.DictComp):
            arg_type.append("Dict")
        elif isinstance(arg, ast.Set):
            arg_type.append("Set")
        elif isinstance(arg, ast.SetComp):
            arg_type.append("Set")
        elif isinstance(arg, ast.Str):
            arg_type.append("Str")
        elif isinstance(arg, ast.NameConstant):
            arg_type.append("NameConstant")
        elif isinstance(arg, ast.Constant):
            arg_type.append("Constant")
        elif isinstance(arg, ast.Call):
            arg_type.append(("Call", get_func_calls_type(arg)[0]))
        else:
            arg_type.append("Other")
    return arg_type


def get_func_calls_type(tree):
    node = deepcopy(tree)
    transformer = TypeInferCallTransformer()
    transformer.visit(node)
    return transformer.call_names


def get_call_type(tree):
    """
    Get the argument types of all function calls
    Args:
        tree: the ast tree being checked

    """
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            call_visitor = FuncCallVisitor()
            call_visitor.visit(node.func)
            func_calls += [(call_visitor.name, get_args(node))]
    return func_calls
