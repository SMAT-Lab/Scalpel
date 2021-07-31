#!/usr/bin/env python
# coding: utf-8
# In[1]:
# a comment starts with "#"
# everything after it is ignored
print("some text to print")
# In[2]:
# string of letters uses quotes
"some string"
'another string'
# number (integer)
1
# number with decimals (float)
1.1
# In[3]:
type("a string")
# In[4]:
# addition
print(1 + 1)
# subtraction
print(5 - 3)
# multiplication
print(2 * 2)
# division
print(6 / 3)
# In[5]:
# define variables by using "="
x = 1            # set x equal to the number 1
y = 2            # assign the number 2 to y
x * y            # the same as 1 * 2
# In[6]:
# you can include the same variable name on both sides of "="
x = 1
x = x + 1
x
# In[7]:
x = ['a', 'b', 'c']
print(x[1])    # gets 'b'
print(x[1:3])  # gets 'b', 'c'
# In[8]:
import math
high = math.ceil(1.2)
print(high)
low = math.floor(1.2)
print(low)
# In[9]:
from math import ceil
ceil(1.2)