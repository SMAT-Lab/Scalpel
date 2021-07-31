#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import matplotlib.pyplot as plt
# In[5]:
df_pm = pd.read_pickle('../data/clean/sud3_pm.pkl')
print(df_pm.columns)
plt.figure(figsize=(13,10))
plt.plot(df_pm['ref'], label="Référence")
plt.plot(df_pm['PM_6182'], label="PM_6182")
plt.plot(df_pm['PM25_6182'], label="PM25_6182")
plt.plot(df_pm['PM_6179'], label="PM_6179")
plt.plot(df_pm['PM25_6179'], label="PM25_6179")
plt.plot(df_pm['PM_617B'], label="PM_617B")
plt.plot(df_pm['PM25_617B'], label="PM25_617B")
plt.title('PM Ref')
plt.legend()
plt.show()
# In[6]:
df_no2 = pd.read_pickle('../data/clean/sud3_no2.pkl')
print(df_no2.columns)
plt.figure(figsize=(13,10))
plt.plot(df_no2['ref'], label="Référence")
plt.plot(df_no2["NO2_61FD"], label="NO2_61FD")
plt.plot(df_no2["NO2_61F0"], label="NO2_61F0")
plt.plot(df_no2["NO2_61EF"], label="NO2_61EF")
plt.title('NO2 Ref')
plt.legend()     
plt.show()