import os
import sys
import ast
import astor
from scalpel.core.module_graph import MNode, ModuleGraph
from scalpel.SSA.ssa import SSA

# we need to define cretieras for variables

def test_ssa():
    filename = sys.argv[1]
    source = open(filename).read()
    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()

    var_records = mnode.parse_vars()
    call_records = mnode.parse_func_calls()
    assert len(var_records) > 0
    assert len(call_records) > 0

    var_records = mnode.parse_vars(scope="get_ident")
    call_records = mnode.parse_func_calls(scope="get_ident")
    assert len(var_records) >  0
    assert len(call_records) > 0

    var_records = mnode.parse_vars(scope="Local")
    call_records = mnode.parse_func_calls(scope="Local")
    #for r in var_records:
    #    print(r)
    assert len(var_records)  > 0
    assert len(call_records) > 0

    var_records = mnode.parse_vars(scope="LocalStack.__call__")
    call_records = mnode.parse_func_calls(scope="LocalStack.__call__")
    assert len(var_records)  > 0
    assert len(call_records) > 0

    ast_node = mnode.ast
    m_ssa = SSA(source)
    m_ssa.gen()
    m_ssa.test()
    pass

def test_SSA():
    filename = sys.argv[1]
    source = open(filename).read()
    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()
    ast_node = mnode.ast
    m_ssa = SSA(source)
    m_ssa.gen()
    m_ssa.test()


if __name__ == '__main__':
    test_SSA()
