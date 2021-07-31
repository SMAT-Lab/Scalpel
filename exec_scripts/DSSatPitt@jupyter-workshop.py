#!/usr/bin/env python
# coding: utf-8
# In[2]:
# Executed code cells have their output displayed below
print('hello world!')
# In[4]:
# plot a sin curve as an image
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 3*np.pi, 500)
plt.plot(x, np.sin(x**2))
plt.title('A simple chirp')
# In[7]:
get_ipython().system('jupyter nbconvert what-is-jupyter --to slides --post serve')