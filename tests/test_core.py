import os
import sys
import ast
import astor
from scalpel.core.mnode import MNode
from scalpel.core.func_call_visitor import get_func_calls
from scalpel.core.vars_visitor import get_vars
from scalpel.SSA.ssa import SSA


# we need to define cretieras for variables
def single_case(code_str, expected_name):
    ast_node = ast.parse(code_str)
    calls = get_func_calls(ast_node)
    assert len(calls)==1
    assert calls[0]['name'] == expected_name


def test_function_calls():
    code_str = """a = fun() """
    single_case(code_str, "fun")

    code_str = """a.fun() """
    single_case(code_str, "a.fun")

    code_str = """a.fun.fun() """
    single_case(code_str, "a.fun.fun")

    code_str = """x+fun().fun() """
    single_case(code_str, "fun.fun")

    code_str = """self.item.fun() """
    single_case(code_str, "self.item.fun")

    code_str = """self._local.__release_local__() """
    single_case(code_str, "self._local.__release_local__")

    code_str = """object.__setattr__(self._local, "__ident_func__", value) """
    single_case(code_str, "object.__setattr__")


def test_get_vars():
    code_str = "ada.fit(X_std, y)"
    ast_node = ast.parse(code_str)
    var_results = get_vars(ast_node)
    var_names = [r['name'] for r in var_results]
    print(var_names)
    assert ("ada" in var_names)
    assert ("X_std" in var_names)
    assert ("y" in var_names)
    code_str = "(errors**2).sum() / 2.0"
    ast_node = ast.parse(code_str)
    var_results = get_vars(ast_node)
    var_names = [r['name'] for r in var_results if r['name'] is not None]
    assert len(var_names) == 1 and "errors" in var_names

    code_str = "return float(len(lcs(a, b))) / max(len(a), len(b))"
    ast_node = ast.parse(code_str)
    var_results = get_vars(ast_node)
    var_names = [r['name'] for r in var_results if r['name'] is not None]
    assert "lcs"  in var_names


def main():
    test_function_calls()
    test_get_vars()


if __name__ == '__main__':
    main()
