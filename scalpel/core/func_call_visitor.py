import ast
from collections import deque
from ast import NodeVisitor
from copy import deepcopy

class CallTransformer(ast.NodeTransformer):
    def __init__(self):
        self.call_names = []
    #def visit_FunctionDef(self, node):
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

def get_args(node):
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
            arg_type.append(("Call", get_func_calls(arg)[0]))
        else:
            arg_type.append("Other")
    return arg_type

def get_call_type(tree):
    # how to remove 
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls += [(callvisitor.name, get_args(node))]
    return func_calls

def get_func_calls(tree):
    node = deepcopy(tree)
    transformer = CallTransformer()
    transformer.visit(node)
    return transformer.call_names

def get_func_calls1(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls += [callvisitor.name]
    return func_calls

#def get_func_calls(tree, extended=False):
#    func_calls = []
#    for node in ast.walk(tree):
#        if isinstance(node, ast.Call):
#            if  (extended==True) or (not isinstance(node.func, ast.Attribute)):  # skip object memeber calls
#                callvisitor = FuncCallVisitor()
#                callvisitor.visit(node.func)
#                func_calls += [callvisitor.name]
        #elif isinstance(node, ast.FunctionDef):
        #    func_calls += [(node.name, "def")]
        #elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Lambda):
        #    func_calls += [(node.targets[0].id, "def")]
    return func_calls
