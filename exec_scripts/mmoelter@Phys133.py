#!/usr/bin/env python
# coding: utf-8
# In[1]:
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
plt.rcParams['font.size'] = 14
def f(n):
    plt.plot([0,1,2],[0,1,n])
    plt.axis([0,2,0,10])
    plt.grid(True)
    plt.show()
interact(f,n=(0,10,1))#,continuous_update = False)