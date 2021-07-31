#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
import sys
import glidepy as gp
plt.ion()
# In[2]:
print(sys.version)
# In[3]:
plt.plot(*np.random.randn(2, 1000))
# In[4]:
a = gp.Test()
# In[5]:
from IPython.display import Image, display
display(Image(filename='img/asw27polar.png', embed=True, width=800, height=800))