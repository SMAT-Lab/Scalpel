#!/usr/bin/env python
# coding: utf-8
# In[8]:
#import libraries, set up the environment
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
# In[9]:
#do the math
#define x
x=np.arange(-10,11)
#calculate some function values for x
f_1 = x**3 + 3*x**2
f_2 = x**3 - 3*x**2
# In[20]:
#do the drawing
#create a new plot
fig, ax = plt.subplots(figsize=(12, 9))
#draw curves for functions
graph_1 = ax.plot(x,f_1,label='f_1')
graph_2 = ax.plot(x,f_2,label='f_2')
#define axes
f_min = np.minimum(f_1,f_2)
f_max = np.maximum(f_1,f_2)
ax.set_xlim(np.min(x), np.max(x))
ax.set_ylim(np.min(f_min), np.max(f_max))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid()
#add a legend 
handles, labels = ax.get_legend_handles_labels()
leg = ax.legend(handles, labels)