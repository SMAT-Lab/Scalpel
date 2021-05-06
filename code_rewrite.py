import os
import sys
import ast
import astor
import astunparse
from scalpel.rewriter import Rewriter

def main():
    src_file = sys.argv[1]
    src = open(src_file).read()
    pattern = lambda x:isinstance(x, ast.Assign)
    new_stmt = []
    rewriter = Rewriter(src, pattern, new_stmt)
    new_ast = rewriter.insert_before()
    #new_ast = rewriter.remove()
    new_ast = rewriter.replace()

    new_src = astor.to_source(new_ast)
    print(new_src)
    return 0

if __name__ == "__main__":
    main()
