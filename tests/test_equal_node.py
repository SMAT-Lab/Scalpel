import os
import ast
from scalpel.cfg.builder import invert


def main():
    src = "a is True"
    src2 = "a is not True"
    src = "a ==0"
    src2 = "a !=0"
    tree1 = ast.parse(src)
    tree2 = ast.parse(src2)
    node1 = tree1.body[0].value
    node2 = tree2.body[0].value
    inv_node = invert(node1)
    print(ast.dump(node1))
    print(ast.dump(inv_node))
    print(ast.dump(node2))
    fields1 = list( ast.iter_fields(node1))
    fields2 =  list(ast.iter_fields(node2))
    l = len(fields1)
    for tmp in ast.walk(node2):
        if hasattr(tmp, "lineno"):
            tmp.lineno=0
        if hasattr(tmp, "col_offset"):
            tmp.col_offset=None
        if hasattr(tmp, "col_offset"):
            tmp.col_offset=None
        if isinstance(tmp, ast.Name):
            tmp.ctx=None
    for tmp in ast.walk(inv_node):
        if hasattr(tmp, "lineno"):
            tmp.lineno=0
        if hasattr(tmp, "col_offset"):
            tmp.col_offset=None
        if hasattr(tmp, "col_offset"):
            tmp.col_offset=None
        if isinstance(tmp, ast.Name):
            tmp.ctx=None

    if inv_node==node2:
        print('testing')

    pass


if __name__ == '__main__':
    main()
