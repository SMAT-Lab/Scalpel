#No phi nodes are placed

a = 10
b = 10
a = 20
b = 20
a += 10
b += 20
print(a)
print(b)

# we need a case when no phi function placed for different blocks
c = 10
if True:
    print(c)
print(c)
