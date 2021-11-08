import os
import sys
import ast
import astor
from scalpel.core.mnode import MNode
from scalpel.SSA.ssa import SSA

def test_SSA():

    filename = sys.argv[1]
    source = open(filename).read()
    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()
    ast_node = mnode.ast
    cfg = mnode.gen_cfg()
    m_ssa = SSA(source)
    m_ssa.compute_SSA(cfg) 
    viz_graph = cfg.build_visual("pdf")
    viz_graph.attr("node", nodesep= "0.5")
    viz_graph.render('cfg.pdf', view=False)


if __name__ == '__main__':
    test_SSA()
