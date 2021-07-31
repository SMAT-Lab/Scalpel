#!/usr/bin/env python
# coding: utf-8
# In[5]:
# Will return the product of x and y, y defaulting to 10
def myfn(x, y = 10):
    return x * y
print(myfn(10)) # 100
print(myfn(3, 3)) # 9
# In[8]:
integer = 1
float = 1.
print(integer / 3)
print(float / 3)
# In[9]:
num = 10
if (num < 10):
    print("Impossible!")
else:
    print("Pew, hell didn't freeze yet")