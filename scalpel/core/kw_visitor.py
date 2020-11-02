import ast
class KWVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = list()

    def visit_keyword(self, node):
        print(node.value)
