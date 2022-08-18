'''
The objective of this script is to check if the constant propagation module is able to detect all possible values of variables. 

'''

from scalpel.cfg.builder import CFGBuilder
from scalpel.SSA.const import SSA
import ast

def test_callable():
    target_file = "tests/test-cases/constant_propagation/callable.py"
    cfg = CFGBuilder().build_from_file(name="callable", filepath=target_file)
    ssa = SSA()
    
    _, const_dict = ssa.compute_SSA(cfg)

    callable_var = next(filter(lambda x: "preprocessing" in x[0][0], const_dict.items()))

    assert callable_var[1]
    assert isinstance(callable_var[1], ast.FunctionDef)


def main():
    test_callable()

if __name__ == '__main__':
    main() 