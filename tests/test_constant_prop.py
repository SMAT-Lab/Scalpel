'''
The objective of this script is to check if the constant propagation module is able to detect all possible values of variables. 
'''

from scalpel.cfg.builder import CFGBuilder
from scalpel.SSA.const import SSA
import ast

def test_tuples():
    target_file = "tests/test-cases/constant_propagation/tuples.py"
    cfg = CFGBuilder().build_from_file(name="callable", filepath=target_file)
    ssa = SSA()
    
    _, const_dict = ssa.compute_SSA(cfg)

    tuple_var_a = next(filter(lambda x: "a" in x[0][0], const_dict.items()))
    tuple_var_b = next(filter(lambda x: "b" in x[0][0], const_dict.items()))
    tuple_var_c = next(filter(lambda x: "c" in x[0][0], const_dict.items()))
    tuple_var_d = next(filter(lambda x: "d" in x[0][0], const_dict.items()))

    assert tuple_var_a[1]
    assert isinstance(tuple_var_a[1], ast.Constant)
    assert tuple_var_b[1]
    assert isinstance(tuple_var_b[1], ast.Constant)
    assert tuple_var_c[1]
    assert isinstance(tuple_var_c[1], ast.Call)
    assert tuple_var_d[1]
    assert isinstance(tuple_var_d[1], ast.Call)


def main():
    test_tuples()

if __name__ == '__main__':
    main() 
