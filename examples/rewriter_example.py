import ast
import os
import sys

import astor

from scalpel.rewriter import Rewriter

src = """
a = list()
b = dict()
"""
expected_src = """
a = []
b = {}
"""


def rewrite_rules(node) -> list:
    if isinstance(node, ast.Assign):
        if isinstance(node.value, ast.Call) and hasattr(node.value.func, "id"):
            if node.value.func.id == "list":
                new_assign_value = ast.List(elts=[], ctx=ast.Load())
                new_stmt = ast.Assign(node.targets, new_assign_value)
                return [new_stmt]
            if node.value.func.id == "dict":
                new_assign_value = ast.Dict(keys=[], values=[])
                new_stmt = ast.Assign(node.targets, new_assign_value)
                return [new_stmt]


def main():
    rewriter = Rewriter()
    new_src = rewriter.rewrite(src, rule_func=rewrite_rules)
    print(new_src)


if __name__ == "__main__":
    main()
