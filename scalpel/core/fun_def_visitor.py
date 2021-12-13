import ast


class FunDefVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = {}

    def visit(self, node):
        print(ast.dump(node))
        self.result['name'] = node.name
        return node
    def visit_Args(self, node):
        print('1111')
