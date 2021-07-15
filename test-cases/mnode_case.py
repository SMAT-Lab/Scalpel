from X import A
from X import B
from X.C import C2
from Y import D as d
from . import Test

def main(a, b):
#def main(a, b, x=10, y=10, z = 10):
    AA(a,b)
    return 0

def AA(a,b):
    BB()
    CC()
    x = d.xx()
    return 0

def BB(a,b):
    CC()
    y = 10
    return 0

def CC(a,b):
    Test.fun(a,b)
    z = 10
    return 0


class Test2(Test):
    def __init__(self, a, b, x=10, y=10, z=10):
        return 0
    def fun(self, x,y,k=10, s=10):
        A.xx(x,y)
        return 0

class Test3:
    class Test4:
        def __init__(self, a, b, x=10, y=10, z=10):
            return 0
    def __init__(self, a, b, x=10, y=10, z=10):
        return 0
    def fun2(self, x,y,k=10, s=10):
        Test4(1,2)
        return 0