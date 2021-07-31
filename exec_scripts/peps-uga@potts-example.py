#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# In[2]:
n = 50
nb_jumps = 4
# In[3]:
j = np.sort(np.random.choice(range(1,n-1),size=nb_jumps-1, replace=False))
v = np.random.rand(nb_jumps)*10
# In[4]:
x = np.zeros(n)
jump = 0
for i in range(n):
    x[i] = v[jump]
    if jump < nb_jumps-1 and i == j[jump]:
            jump += 1
# In[5]:
sigma = 0.03*max(v)
y = x + sigma*np.random.randn(n)
# In[6]:
plt.plot(x , 'k*',label="original signal")
plt.plot(y , 'b',label="noisy signal")
plt.legend()
# In[7]:
import lib.Potts as lp 
# In[8]:
p = lp.L2_Potts(y,0.7)
# In[9]:
plt.plot(x , 'k*',label="original signal")
plt.plot(y , 'b',label="noisy signal")
plt.plot(p , 'r',label="L2 Potts recovery")
plt.legend()
# In[10]:
import lib.Potts as lp 
# In[11]:
p1 = lp.L1_Potts(y,0.9)
# In[12]:
plt.plot(x , 'k*',label="original signal")
plt.plot(y , 'b',label="noisy signal")
plt.plot(p1 , 'r',label="L1 Potts recovery")
plt.legend()