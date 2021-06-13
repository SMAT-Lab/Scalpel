class A:
   def fun(self): 
       return 0

class B:
   def fun(self): 
       return 0

#def test_fun(s):
#    if isinstance(s, str):
#        return s
#    return None

a = 10
obj = A()

if a>0:
    #obj = B()
    a = 20
else:
    obj = B()
    a = 30

s = obj.fun() +a

