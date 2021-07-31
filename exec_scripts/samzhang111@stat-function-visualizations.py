#!/usr/bin/env python
# coding: utf-8
# In[6]:
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# In[7]:
import numpy as np
inputs = np.arange(-3, 3, 0.01)
# In[8]:
import math
def sigmoid(array):
    return [1/(1 + math.e ** (-x)) for x in array]
plt.plot(inputs, sigmoid(inputs))
# In[9]:
def tanh(array):
    def numerator(x):
        return (1 - math.e ** (-2 * x))
    def denominator(x):
        return ( 1 + math.e ** (-2 * x))
    return [numerator(x)/denominator(x) for x in array]
plt.plot(inputs, tanh(inputs))
# In[10]:
from collections import Counter
def gini_impurity(array):
    counter = Counter(array)
    keys = counter.keys()
    counts = list(counter.values())
    size = float(len(array))
    gini = 0.0
    for i, key in enumerate(keys):
        f_i = counts[i]/size
        gini += (f_i - f_i ** 2)
    return gini
i_s = []
ginis = []
for i in range(1, 100):
    inputs = [1] * i + [2]
    
    i_s.append(i)
    ginis.append(gini_impurity(inputs))
    
plt.plot(i_s, ginis)