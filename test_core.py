import os
import sys
import ast
import astor
from scalpel.core.module_graph import MNode, ModuleGraph
from scalpel.core.func_call_visitor import get_func_calls
from scalpel.SSA.ssa import SSA

# we need to define cretieras for variables
def test_single_case(code_str, expected_name):
    ast_node = ast.parse(code_str)
    calls = get_func_calls(ast_node)
    assert len(calls)==1
    assert calls[0]['name'] == expected_name

def test_function_calls():
    code_str = """a = fun() """
    test_single_case(code_str, "fun")

    code_str = """a.fun() """
    test_single_case(code_str, "a.fun")

    code_str = """a.fun.fun() """
    test_single_case(code_str, "a.fun.fun")

    code_str = """x+fun().fun() """
    test_single_case(code_str, "fun.fun")

    code_str = """self.item.fun() """
    test_single_case(code_str, "self.item.fun")

    code_str = """self._local.__release_local__() """
    test_single_case(code_str, "self._local.__release_local__")

    code_str = """object.__setattr__(self._local, "__ident_func__", value) """
    test_single_case(code_str, "object.__setattr__")

if __name__ == '__main__':
    test_function_calls()
