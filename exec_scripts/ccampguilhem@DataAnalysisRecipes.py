#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
# In[2]:
df1 = pd.DataFrame({"City": ["Paris", "London", "New York", "Tokyo"],
                    "Population": [12475808, 12317800, 20182305, 42794714],
                    "Country": ["France", "UK", "USA", "Japan"]})
df1.head()
# In[3]:
df2 = pd.DataFrame({"Country": ["France", "UK", "USA", "China"],
                    "Population": [67595000, 65110000, 324811000, 1376049000]})
df2.head()
# In[4]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"))
result.head()
# In[5]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='inner')
result.head()
# In[6]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='left')
result.head()
# In[7]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='right')
result.head()
# In[8]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='outer')
result.head()
# In[9]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='outer', indicator=True)
result.head()
# In[10]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='outer', indicator=True)
result = result[result["_merge"] != "both"]
result.head()
# In[11]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='left', indicator=True)
result = result[result["_merge"] == "left_only"]
result.head()
# In[12]:
result = pd.merge(df1, df2, on="Country", suffixes=("_city", "_country"), how='right', indicator=True)
result = result[result["_merge"] == "right_only"]
result.head()