#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
# In[2]:
measurements_df = pd.read_csv("Resources/hawaii_measurements.csv")
stations_df = pd.read_csv("Resources/hawaii_stations.csv")
# In[3]:
print(f"Initial shape - Measurements - {measurements_df.shape}")
print(f"Initial shape - Stations - {stations_df.shape}")
# In[4]:
measurements_df.head()
# In[5]:
stations_df.head()
# In[6]:
measurements_df = measurements_df.dropna(how='any')
stations_df = stations_df.dropna(how='any')
# In[7]:
print(f"Current shape - Measurements - {measurements_df.shape}")
print(f"Current shape - Stations - {stations_df.shape}")
# In[8]:
measurements_df = measurements_df.reset_index()
stations_df = stations_df.reset_index()
# In[9]:
measurements_df.to_csv("Cleaned/clean_hawaii_measurements.csv")
stations_df.to_csv("Cleaned/clean_hawaii_stations.csv")