import ast
import os
import sys

import astor

from scalpel.rewriter import Rewriter

src = """
def func(a,b):
    c = a+b
    return c
"""

target = """
def func(x,y):
    z = x+y
    return z
"""


def rewrite_rules(node) -> list:
    old_name = "c"
    new_name = "z"
    for tmp_node in ast.walk(node):
        if isinstance(tmp_node, ast.Name):
            if tmp_node.id == old_name:
                tmp_node.id = new_name
    return [node]


def main():
    rewriter = Rewriter()
    new_src = rewriter.rewrite(src, rule_func=rewrite_rules)
    print(new_src)


if __name__ == "__main__":
    main()
