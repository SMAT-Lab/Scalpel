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


def test_enumerate():
    target_file = "tests/test-cases/constant_propagation/enumerate.py"

    cfg = CFGBuilder().build_from_file(name="enumerate", filepath=target_file)
    ssa = SSA()

    _, const_dict = ssa.compute_SSA(cfg)

    enumerate_count = next(filter(lambda x: "count" in x[0][0], const_dict.items()))
    enumerate_value = next(filter(lambda x: "value" in x[0][0], const_dict.items()))

    assert enumerate_count[1]
    assert isinstance(enumerate_count[1], ast.Call)
    assert enumerate_value[1]
    assert isinstance(enumerate_value[1], ast.Call)


def test_callable():
    target_file = "tests/test-cases/constant_propagation/callable.py"
    cfg = CFGBuilder().build_from_file(name="callable", filepath=target_file)
    ssa = SSA()

    _, const_dict = ssa.compute_SSA(cfg)

    callable_var = next(filter(lambda x: "preprocessing" in x[0][0], const_dict.items()))

    assert callable_var[1]
    assert isinstance(callable_var[1], ast.FunctionDef)


def test_instance_variable():
    target_file = "tests/test-cases/constant_propagation/instance_variables.py"
    cfg = CFGBuilder().build_from_file(name="instance_variable", filepath=target_file)
    ssa = SSA()

    const_dict = {}

    for class_cfg in cfg.class_cfgs.values():
        for func_cfg in class_cfg.functioncfgs.values():
            _, _dict = ssa.compute_SSA(func_cfg)
            const_dict.update(_dict)

    instance_var = next(filter(lambda x: "self.x" in x[0][0], const_dict.items()))
    
    assert instance_var[1]
    assert isinstance(instance_var[1], ast.Constant)


def main():
    test_tuples()
    test_enumerate()
    test_callable()


if __name__ == '__main__':
    main() 
