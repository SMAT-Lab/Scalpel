
from . import A
from . import B
from . import C
from .. import D

def main(a, b):
#def main(a, b, x=10, y=10, z = 10):
    AA()
    return 0

def AA(a,b):
    BB()
    x = 0
    return 0

def BB(a,b):
    CC()
    y = 10
    return 0

def CC(a,b):
    Test()
    z = 10
    return 0


class Test:
    def __init__(self, a, b, x=10, y=10, z=10):
        return 0
    def fun(self, x,y,k=10, s=10):
        return 0
