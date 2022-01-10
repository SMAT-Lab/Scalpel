import ast
from .class_visitor import ClassVisitor
from .fun_def_visitor import FunDefVisitor


def get_keywords(node):
    args = node.args
    arg_names = []
    defaults = args.defaults
    for arg in args.args:
        arg_names += [arg.arg]
    return arg_names, len(defaults)


class SourceVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = {}
        self.pair = {}

    def visit_FunctionDef(self, node):
        kw_names = get_keywords(node)
        self.result[node.name] = kw_names
        return node

    def visit_ClassDef(self, node):
        visitor = ClassVisitor()
        visitor.visit(node)
        if len(node.bases)>0:
            if hasattr(node.bases[0],"id"):
                self.pair[node.name] = node.bases[0].id
        else:
            self.pair[node.name] = None
        self.result[node.name] = visitor.result
        return node
