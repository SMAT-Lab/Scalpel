import ast
import os
import sys
import unittest

import astor

from scalpel.core.mnode import MNode
from scalpel.SSA.const import SSA

code_str = """
b = 10
if b>0:
    a = a+b
else:
    a = 10
print(a)
"""


def main():
    mnode = MNode("local")
    mnode.source = code_str
    mnode.gen_ast()
    cfg = mnode.gen_cfg()
    m_ssa = SSA()
    ssa_results, const_dict = m_ssa.compute_SSA(cfg)
    for block_id, stmt_res in ssa_results.items():
        print("These are the results for block ".format(block_id))
        print(stmt_res)
    for name, value in const_dict.items():
        print(name, value)
    print(ssa_results)


if __name__ == "__main__":
    main()
