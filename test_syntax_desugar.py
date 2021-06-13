import os
import sys
import ast
import astor
from scalpel.core.module_graph import MNode, ModuleGraph
from scalpel.rewriter import Rewriter
from scalpel.SSA.ssa import SSA

# we need to define cretieras for variables
def test_syntax_desugar():
    filename = sys.argv[1]
    source = open(filename).read()
    print(source)
    rewriter = Rewriter(source)
    new_ast = rewriter.rewrite()
    #new_ast = ast.fix_missing_locations(mnode.ast)
    new_src = astor.to_source(new_ast)
    print(new_src)

if __name__ == '__main__':
    test_syntax_desugar()
