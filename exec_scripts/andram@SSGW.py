#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
import SSGW
from ipywidgets import interact
np.seterr(all="ignore")
@interact(Hd=(0,2,0.01),Ld_log10=(0,4,0.1))
def myplot(Hd=0.5, Ld_log10=2, N_log2=11 ):
    Ld = 10**Ld_log10
    N = 2**N_log2
    kd=2*np.pi/Ld 
    kH2=np.pi*Hd/Ld 
    # print(f"Hd = {Hd}, Ld = {Ld:5.4f}, N = {N}")
    # commenting out above line to avoid display flicker
    [zs,ws,PP]=SSGW.SSGW(kd, kH2, N);
    
    
# In[2]:
[zs,ws,PP] = SSGW.SSGW(np.inf,0.3)
# In[3]:
Hd=0.5; Ld=100; kd=2*np.pi/Ld; kH2=np.pi*Hd/Ld; [zs,ws,PP]=SSGW.SSGW(kd,kH2)
# In[4]:
# The following takes over a minute to run, which is not appropriate for a public server.
#Hd=0.7; Ld=10000; kd=2*np.pi/Ld; kH2=np.pi*Hd/Ld; [zs,ws,PP]=SSGW.SSGW(kd,kH2,2**19);