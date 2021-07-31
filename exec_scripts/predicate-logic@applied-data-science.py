#!/usr/bin/env python
# coding: utf-8
# In[30]:
import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# In[20]:
s1 = pd.Series([1,2,3])
s1
# In[35]:
s2 = pd.Series([1,2,3, np.nan])
s2
# In[33]:
s2.dropna().apply(int)
# In[34]:
s3 = pd.Series([1,True,'a', np.pi])
s3