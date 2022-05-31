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
        assert ('a' in ssa_results[3][2] and len(ssa_results[3][2]['a'])==4)
        assert ('b' in ssa_results[3][2] and len(ssa_results[3][2]['b'])==3)

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
        assert ('t' in ssa_results[3][0] and len(ssa_results[3][0]['t'])==1)
    def test_case_4(self):
        filename = "tests/test-cases/ssa_basecase/ssa_case_4.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        assert ("count",0) in const_dict
        assert ("count",1) in const_dict
    def test_case_5(self):
        filename = "tests/test-cases/ssa_basecase/ssa_case_10.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        assert ('url', 0) in const_dict and const_dict[('url',0)] is None
    def test_case_6(self):
        filename = "tests/test-cases/ssa_basecase/ssa_case_9.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        assert ('result',1) in const_dict
        assert const_dict[('result',1)] is not None

    def test_case_7(self):
        filename = "tests/test-cases/ssa_basecase/ssa_case_11.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        assert len(ssa_results) == 4 # 4 blocks
        assert ssa_results[1] == [{}, {'isinstance': set(), 'a': {0}, 'int': set()}]
        assert ssa_results[2] == [{}]
        assert ssa_results[4] == [{}]
        assert ssa_results[3] == [{}, {'a': {0}, 'b': {2}}]


    def test_case_8(self):
        filename = "tests/test-cases/ssa_basecase/ssa_case_12.py"
        source = open(filename).read()
        mnode = MNode("local")
        mnode.source = source
        mnode.gen_ast()
        ast_node = mnode.ast
        cfg = mnode.gen_cfg()
        graph = cfg.build_visual('pdf')
        graph.render("example_cfg.pdf", view=False)
        m_ssa = SSA()
        ssa_results, const_dict = m_ssa.compute_SSA(cfg) 
        assert  ("a", 0) in const_dict
        assert  ("b", 0) in const_dict



if __name__ == '__main__':
    unittest.main()
