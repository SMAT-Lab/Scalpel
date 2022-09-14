import ast
from .fun_def_visitor import FunDefVisitor

def get_keywords(node):
    args = node.args
    arg_names = []
    defaults = args.defaults
    for arg in args.args:
        arg_names += [arg.arg]
    return arg_names, len(defaults)


class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = {}

    def visit_ClassDef(self, node): 
        return node


