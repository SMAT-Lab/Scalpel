from X import testX
class A:
   def fun(self): 
       return 0

class B:
   def fun(self): 
       return 0

def test_fun():
    return 0

a = 10
#obj = A()

obj = None

if a>0:
    obj = B()
    c = 0
    a = 20
else:
    #c = 2 
    #obj = B()
    a = 30

# def-use chain anaysis
# undefined variable 
# type check 
# nameerror c not found 
s = obj.fun() +a + c

obj.fun()

