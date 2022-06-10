import sys
import ast
from collections import deque
from ast import NodeVisitor
from copy import deepcopy


def is_py38_or_higher():
    if sys.version_info.major == 3 and sys.version_info.minor >= 8:
        return True
    return False


NAMECONSTANT_TYPE = ast.Constant if is_py38_or_higher() else ast.NameConstant


class CallTransformer(ast.NodeTransformer):
    def __init__(self):
        self.call_names = []

    def visit_Attribute(self, node):
        #        self.generic_visit(node.value)
        return node

    def param2str(self, param):

        def get_func(node):
            if type(node) == ast.Name:
                return node.id
            elif type(node) == ast.Constant:
                # ingore such as  "this is a constant".join()
                return ""
            elif type(node) == ast.BinOp:
                # ingore such as  (a+b+c).fun()
                return ""
            elif type(node) == ast.Subscript:
                # currently, we will ignore the slices because we cannot track the type of the value.
                # for instance,  a[something].fun() ->  a.fun()
                # this sacrifice
                return get_func(node.value)  
            #elif type(node) == ast.JoinedStr:
            #    return ""
            elif type(node) == ast.Attribute:
                if type(node.value) in [ast.JoinedStr, ast.Constant]:
                    return node.attr
                else:
                    return get_func(node.value) + "." + node.attr 
            elif type(node) == ast.Call:
                return get_func(node.func)
            elif type(node) == ast.IfExp:
                return ""
            elif type(node) == ast.Compare:
                return ""
            elif type(node) == ast.UnaryOp:
                return ""
            #ast.UnaryOp
            else:
                #import astor
                #print(astor.to_source(node))
                raise Exception(str(type(node)))
    
        if isinstance(param, ast.Subscript):
            return self.param2str(param.value)
        if isinstance(param, ast.Call):
            return get_func(param)
        elif isinstance(param, ast.Name):
            return param.id
        elif isinstance(param, ast.Num):
            # python 3.6  
            return param.n
            #return param.value
        elif isinstance(param, ast.List):
            return "List"
        elif isinstance(param, ast.ListComp):
            return "List"
        elif isinstance(param, ast.Tuple):
            return "Tuple"
        elif isinstance(param, (ast.Dict, ast.DictComp)):
            return "Dict"
        elif isinstance(param, (ast.Set, ast.SetComp)):
            return "Set"
        elif isinstance(param, ast.Str):
            return param.s
        elif isinstance(param, ast.NameConstant):
            return param.value
        elif isinstance(param, ast.Constant):
            return param.value
        elif isinstance(param, ast.Expr):
            return "Expr"
        else:
            return "unknown"

    def visit_Call(self, node):

        tmp_fun_node = deepcopy(node)
        tmp_fun_node.args = []
        tmp_fun_node.keywords = []

        callvisitor = FuncCallVisitor()
        callvisitor.visit(tmp_fun_node)

        call_info = {"name": callvisitor.name,
                     "lineno": tmp_fun_node.lineno,
                     "col_offset": tmp_fun_node.col_offset,
                     "params": []
                     }
        self.call_names += [call_info]
        for arg in node.args:
            call_info["params"] += [self.param2str(arg)]
            self.generic_visit(arg)

        for kw in node.keywords:
            call_info["params"] += [self.param2str(kw.value)]
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


    def visit_Subscript(self, node):
        # ingore subscription slice 
        self.visit(node.value)
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
