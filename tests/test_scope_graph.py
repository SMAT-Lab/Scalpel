import os
import ast
import sys
from scalpel.scope_graph import ScopeGraph
src = """
class A:
    static_a = 0
    def fun1():
        a = 0
        pass 
    def fun2():
        a = static_a +1
class B:
    def fun1():
        pass 
    def fun2():
        pass 

class C(B, A):
    def __int__(self):
        return super().fun1()

obj_a = C()
c.fun1()

"""

src =  """

class A:
    def rk(self):
        print(" In class A")
class B(A):
    def rk(self):
        print(" In class B")
class C(A):
    def rk(self):
        print("In class C")


class D(B, C):
    pass
    
"""


def main():
    ast_tree = ast.parse(src)
    sg = ScopeGraph()
    sg.build(ast_tree)
    sg.test()
    sg.print_out()
    sg.test_MRO_resolve("D")


if __name__ == "__main__":
    main()


