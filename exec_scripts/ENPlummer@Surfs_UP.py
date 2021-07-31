#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
# In[2]:
measurements = pd.read_csv("Resources/hawaii_measurements.csv")
measurements.head()
# In[3]:
stations = pd.read_csv("Resources/hawaii_stations.csv")
stations.head()
# In[4]:
stations.count()
# In[5]:
measurements.count()
# In[6]:
measurements.to_csv("clean_measurements.csv", index=False)
# In[7]:
stations.to_csv("clean_stations.csv", index=False)