# lambda 
fun = lambda x:x**2

# simple listcomp

lst = [int(a) for a in lst]

# compound listcomp

lst = [int(a) for a in lst if  a % 2 == 0]

# nested function calls 

s = fun(fun(), [str(a) for a in lst])

# subscription
s = [str(a) for a in lst if a%2==0][0:3]

a = 10

obj = fun(a)

---------------------------
def fun(x):
    return x ** 2


_hidden_lst = []
for a in lst:
    _hidden_lst.append(int(a))
lst = _hidden_lst
_hidden_lst = []
for a in lst:
    if a % 2 == 0:
        _hidden_lst.append(int(a))
lst = _hidden_lst

_hidden_res_14_8 = fun()
_hidden_res_14_15 = []

for a in lst:
    _hidden_res_14_15.append(str(a))
s = fun(_hidden_res_14_8, _hidden_res_14_15)

_hidden_s = []
for a in lst:
    if a % 2 == 0:
        _hidden_s.append(str(a))
s = _hidden_s[0:3]

a = 10
obj = fun(a)
