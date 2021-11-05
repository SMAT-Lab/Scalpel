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

def test_code_rewrite():
    filename = sys.argv[1]
    source = open(filename).read()
    call_node = ast.Call(ast.Name(id='print',ctx=ast.Load()),
            [ast.Constant("testing", None)], [])
    new_stmt = ast.Expr(call_node)

    mnode = MNode("local")
    mnode.source = source
    mnode.gen_ast()
    walker = mnode.make_unit_walker()
    for unit in walker:
        unit.insert_after(new_stmt)

    new_ast = ast.fix_missing_locations(mnode.ast)
    new_src = astor.to_source(new_ast)
    print(new_src)

def main():

    ep = "../lib-type-infe/Lib-Type/top-10/Werkzeug/tmp/werkzeug/"
    top_level_name = "werkzeug"

    m_graph = ModuleGraph(ep, top_level_name)
    m_graph.build()

    working_queue = []
    working_queue.append(m_graph.root_node)
    all_nodes = []
    leaf_stack = []

    # build leaf stack
    while len(working_queue)>0:
        tmp_node = working_queue.pop(0)
        if tmp_node.name.endswith('.py') == True:
            leaf_stack.append(tmp_node)
        working_queue.extend(tmp_node.children)
    test_node = leaf_stack[11]
    print(test_node.name)
    #test_node.gen_ast()
    #import_records = test_node.parse_import_stmt()


    #var_records = test_node.parse_vars()
    #print(var_records)
    #func_call_records = test_node.parse_func_calls()
    #def_records = test_node.parse_func_defs()
    #for r in def_records:
    #    print(r)
    #print(func_call_records)
    return 0

if __name__ == '__main__':
    #main()
    #test_ssa()
    test_SSA()
    #test_code_rewrite()
