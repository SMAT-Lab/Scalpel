from unittest import TestCase
from textwrap import dedent
import gast as ast
import scalpel._duc as beniget


class Capture(ast.NodeVisitor):
    def __init__(self, module_node):
        self.chains = beniget.DefUseChains()
        self.chains.visit(module_node)
        self.users = set()
        self.captured = set()

    def visit_FunctionDef(self, node):
        for def_ in self.chains.locals[node]:
            self.users.update(use.node for use in def_.users())
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            if node not in self.users:
                # FIXME: IRL, should be the definition of this use
                self.captured.add(node.id)


class TestCapture(TestCase):
    def checkCapture(self, code, extract, ref):
        module = ast.parse(dedent(code))
        c = Capture(module)
        c.visit(extract(module))
        self.assertEqual(c.captured, ref)

    def test_simple_capture(self):
        code = """
            def foo(x):
                def bar():
                    return x"""
        self.checkCapture(code, lambda n: n.body[0].body[0], {"x"})

    def test_no_capture(self):
        code = """
            def foo(x):
                def bar(x):
                    return x"""
        self.checkCapture(code, lambda n: n.body[0].body[0], set())
