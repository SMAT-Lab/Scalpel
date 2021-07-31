#!/usr/bin/env python
# coding: utf-8
# In[1]:
def fibonacci(n=10):
    if n == 0: return [0]
    elif n == 1: return [0, 1]
    else:
        r = fibonacci(n - 1)
        return r + [r[-2] + r[-1]]
print(fibonacci(10))
# In[2]:
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import seaborn
pd.Series(fibonacci(10)).plot(kind='bar');