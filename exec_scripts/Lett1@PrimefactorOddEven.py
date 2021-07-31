#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().system('pip install matplotlib sympy')
# In[2]:
get_ipython().run_line_magic('matplotlib', 'nbagg')
import matplotlib.pyplot as plt
import numpy as np
from sympy.ntheory import factorint
# In[3]:
data = []
for x in range(1, 500000):
    decomposits = factorint(x)
    data.append((x, decomposits, len(decomposits) % 2 == 0, len(decomposits) % 2 != 0))
    
data
# In[12]:
evens = np.array([x[2] for x in data])
evens = np.cumsum(evens)
odds = np.array([x[3] for x in data])
odds = np.cumsum(odds)
plt.plot(evens,label="Gerade")
plt.plot(odds,label="Ungerade")
plt.legend()
# In[17]:
plt.close()
plt.plot(np.trim_zeros(evens > odds, 'b'))
# In[10]:
np.where((evens > odds) == True)