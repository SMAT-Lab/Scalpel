#!/usr/bin/env python
# coding: utf-8
# In[10]:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
# In[14]:
data = np.loadtxt('data.txt')
plt.plot(data[:,0], data[:,1])