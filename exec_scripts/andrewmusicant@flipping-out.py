#!/usr/bin/env python
# coding: utf-8
# In[67]:
import math
import random
import statistics as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn
get_ipython().run_line_magic('matplotlib', 'inline')
record = []
heads_record = []
tails_record = []
def flip_coin():
    x = random.randint(1, 2)
    return x
def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)
def simulation():
    count = 0
    heads = 0
    tails = 0
    n = 2**16
    while count < n:
 
        x = flip_coin()
        if is_power2(count):
            heads_record.append(heads)
            tails_record.append(tails)
        if x == 1:
            heads += 1
        else:
            tails += 1
        count += 1
    return heads, tails
x, y = simulation()
points = list(zip(heads_record, tails_record))
difference_points = [x1 - x2 for (x1, x2) in zip(heads_record, tails_record)]
ratio_points = [x1 / x2 for (x1, x2) in zip(heads_record, tails_record) if x2 != 0]
print(points)
print("heads", x, "tails", y)
# print(record)
# In[68]:
plt.plot(difference_points)
plt.show()
# In[69]:
plt.plot(ratio_points)
plt.show()
# In[70]:
# plt.scatter(single_points)
# plt.xscale('log', basex = 2)
# plt.xlabel("logarithmic")
# plt.ylabel("heads tails")
# plt.title("flips")
# plt.show()
# In[71]:
differences = []
for heads, tails in points:
    differences.append(math.fabs(heads - tails))
x_values = []
for num in range(len(differences)):
    x_values.append(2**num)
    
plt.scatter(x_values, differences)
plt.xscale('log', basex = 2)
plt.show()
# In[72]:
ratios = []
for heads, tails in points:
    if tails != 0:
        ratios.append(math.fabs(heads / tails))
x_values = []
for num in range(len(ratios)):
    x_values.append(2**num)
    
plt.scatter(x_values, ratios)
plt.xscale('log', basex = 2)
plt.show()