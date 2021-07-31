#!/usr/bin/env python
# coding: utf-8
# In[3]:
get_ipython().run_line_magic('matplotlib', 'notebook')
# In[2]:
import matplotlib.pyplot as plt
import numpy as np
def pp(ax, point, **kwargs):
    ax.plot([0, point[0]], [0,point[1]], [0, point[2]], **kwargs)
    
    