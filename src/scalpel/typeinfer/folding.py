"""Constant folding of expressions.
This is an implementation of expression node evaluation. The function serves as an alternative to ast.literal_eval().
For example, 4 + 5 can be constant folded into 9. 
"""

from __future__ import annotations
import operator
import ast 
import math 
import builtins

from typing import Union
from typing_extensions import Final


# All possible result types of constant folding
ConstantValue = Union[int, bool, float, str]
CONST_TYPES: Final = (int, bool, float, str)


MATH_FUNCTIONS = [x for x in dir(math) if not "__" in x]
BUILT_IN_FUNCTIONS = [x for x in dir(builtins) if not "__" in x]


BinOps = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

UnaryOps = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.UnaryOp: ast.UnaryOp,
        ast.Not: operator.__not__
    }

ops = tuple(BinOps) + tuple(UnaryOps)


def ast_node_eval(node):
   
    ##TODO
    pass


def _eval(expr):
    if isinstance(expr, ast.Constant):
        return expr.value 
    if isinstance(expr, ast.Num):
        return expr.n 
    if isinstance(expr, ast.Str):
        return expr.s 
    if isinstance(expr, ast.Bytes):
        return expr.s 
    if isinstance(expr, ast.NameConstant):
        return expr.value 
    if isinstance(expr, ast.BinOp):
        op_func = BinOps[type(expr.op)]
        left_val = _eval(expr.left)
        right_val = _eval(expr.right)
        if left_val and right_val:
            return op_func(left_val, right_val)
        return None 
    if isinstance(expr, ast.UnaryOp):
        op_func = UnaryOps[type(expr.op)]
        oprand_val = _eval(expr.operand)
        if oprand_val:
            return op_func(oprand_val)
        return None 
    

def constant_folding(ast_expr):
 
    return _eval(ast_expr)
def src_to_node(src):
    tree = ast.parse(src, mode="eval")
    return tree.body

def tests():
    assert constant_folding(src_to_node("1+1")) == 2
    assert constant_folding(src_to_node("1+-5"))== -4
    assert constant_folding(src_to_node("-1")) == -1
    assert constant_folding(src_to_node("-+1")) == -1
    assert constant_folding(src_to_node("(100*10)+6")) == 1006
    assert constant_folding(src_to_node("100*(10+6)")) == 1600
    assert constant_folding(src_to_node("2**4")) == 2**4
    assert constant_folding(src_to_node("1.2345 * 10")) == 1.2345 * 10
    assert constant_folding(src_to_node('"a"*10')) == "aaaaaaaaaa"
    assert constant_folding(src_to_node('a*10')) == None

tests() 