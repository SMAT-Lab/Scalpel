a = 10
dict_var1 = dict()
dict_var2 = {}

if a>10:
    a = 100
    b = 20
elif a>20:
    a += 20
    b = 21
elif a>30:
    a += 20
elif a>50:
    a += 40
else:
    b = 20

obj_a = classA()
obj_a.var = 0

print(a, b)
