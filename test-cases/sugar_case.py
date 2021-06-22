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

