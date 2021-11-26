import os
import sys
import ast
import astor
import unittest
from scalpel.core.mnode import MNode
from scalpel.SSA.const import SSA


class BaseCaseTests(unittest.TestCase):

    def test_case_1(self):

        filename = "tests/test-cases/ssa_basecase/ssa_case6.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        # three blocks
        assert len(ssa_results) == 3 
        # 1st block, 3rd statement 
        #print(ssa_results)
        assert 'a' in ssa_results[1][2]
        assert 'a' in ssa_results[1][6]
        assert 'a' in ssa_results[1][10]
        assert 'c' in ssa_results[2][0]
        assert 'c' in ssa_results[3][0]
        
    def test_case_2(self):
        filename = "tests/test-cases/ssa_basecase/ssa_case-5.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        print(ssa_results)
        assert len(ssa_results) == 10
        assert ('a' in ssa_results[3][2] and len(ssa_results[3][2]['a'])==5)
        assert ('b' in ssa_results[3][2] and len(ssa_results[3][2]['b'])==4)

    def test_case_3(self):
        filename = "tests/test-cases/ssa_basecase/ssa_case7.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        print(ssa_results)
        assert len(ssa_results) == 4
        assert ('c' in ssa_results[1][1] and len(ssa_results[1][1]['c'])==1)
        assert ('c' in ssa_results[2][0] and len(ssa_results[2][0]['c'])==1)
        assert ('t' in ssa_results[3][0] and len(ssa_results[3][0]['t'])==2)

if __name__ == '__main__':
    unittest.main()


    
    #viz_graph = cfg.build_visual("pdf")
    #viz_graph.attr("node", nodesep= "0.5")
    #viz_graph.render('cfg.pdf', view=False)
