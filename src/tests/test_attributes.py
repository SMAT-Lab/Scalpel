from unittest import TestCase
from textwrap import dedent
import gast as ast
import scalpel.duc as beniget


class Attributes(ast.NodeVisitor):
    def __init__(self, module_node):
        self.chains = beniget.DefUseChains()
        self.chains.visit(module_node)
        self.attributes = set()
        self.users = set()

    def visit_ClassDef(self, node):
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                self_def = self.chains.chains[stmt.args.args[0]]
                self.users.update(use.node for use in self_def.users())
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.value in self.users:
            self.attributes.add(node.attr)


class TestAttributes(TestCase):
    def checkAttribute(self, code, extract, ref):
        module = ast.parse(dedent(code))
        c = Attributes(module)
        c.visit(extract(module))
        self.assertEqual(c.attributes, ref)

    def test_simple_attribute(self):
        code = """
            class F:
                def bar(self):
                    return self.bar"""
        self.checkAttribute(code, lambda n: n.body[0], {"bar"})

    def test_no_attribute(self):
        code = """
            class F(object):
                def bar(self):
                    return 1"""
        self.checkAttribute(code, lambda n: n.body[0], set())

    def test_non_standard_self(self):
        code = """
            class F:
                def bar(fels):
                    return fels.bar + fels.foo"""
        self.checkAttribute(code, lambda n: n.body[0], {"bar", "foo"})

    def test_self_redefinition(self):
        code = """
            class F:
                def bar(self, other):
                    self.foo = 1
                    self = other
                    return self.bar"""
        self.checkAttribute(code, lambda n: n.body[0], {"foo"})

    def test_self_redefinition_in_args(self):
        code = """
            class F:
                def bar(self, self):
                    self.foo = 1"""
        self.checkAttribute(code, lambda n: n.body[0], set())

    def test_self_redefinition_in_branch_true(self):
        code = """
            class F:
                def bar(self, other):
                    if other:
                        self = other
                    self.foo = 1"""
        self.checkAttribute(code, lambda n: n.body[0], {"foo"})

    def test_self_redefinition_in_branch_false(self):
        code = """
            class F:
                def bar(self, other):
                    if not other:
                        pass
                    else:
                        self = other
                    self.foo = 1"""
        self.checkAttribute(code, lambda n: n.body[0], {"foo"})

    def test_self_redefinition_in_both_branch(self):
        code = """
            class F:
                def bar(self, other):
                    if other:
                        self = other
                    else:
                        self = list
                    return self.pop"""
        self.checkAttribute(code, lambda n: n.body[0], set())
