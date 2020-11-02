import ast
from collections import deque
from ast import NodeVisitor

class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return ('.'.join(self._name), "load")

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

def get_func_calls(tree, extended=False):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if  (extended==True) or (not isinstance(node.func, ast.Attribute)):  # skip object memeber calls
                callvisitor = FuncCallVisitor()
                callvisitor.visit(node.func)
                func_calls += [callvisitor.name]
        elif isinstance(node, ast.FunctionDef):
            func_calls += [(node.name, "def")]
        elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Lambda):
            func_calls += [(node.targets[0].id, "def")]
    return func_calls
