import os
import sys
import ast
import astor
from scalpel.core.mnode import MNode
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
    m_final_idents = m_ssa.compute_final_idents()
    #print(m_final_idents)
    #cfg.build_visual('cfg', 'pdf')
    for fun_name, fun_cfg in cfg.functioncfgs.items():
        fun_ssa = SSA(source)
        fun_ssa.compute_SSA(fun_cfg) 
        fun_ssa.test()
    for class_name, class_cfg in cfg.class_cfgs.items():
        # class body ssa compute 
        c_ssa = SSA(source)
        c_ssa.compute_SSA(class_cfg) 
        c_final_idents = c_ssa.compute_final_idents()
        #print(c_final_idents)
        live_idents = []
        for inside_fun_name, inside_fun_cfg in class_cfg.functioncfgs.items():
            #if inside_fun_name == 'status_printer':
            #    inside_fun_cfg.build_visual('cfg', 'pdf')
            live_ident_table = [m_final_idents, c_final_idents]
            fun_ssa = SSA(source)
            fun_ssa.compute_SSA(inside_fun_cfg) 
            fun_ssa.test(live_ident_table=live_ident_table)
            #print(class_name, inside_fun_name)
            #inside_fun_cfg.build_visual('cfg', 'pdf')
            #break

if __name__ == '__main__':
    test_SSA()
