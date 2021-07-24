#!/usr/bin/env python
# coding: utf-8
# In[2]:
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
try:
    xrange
except NameError:
    xrange = range
from __future__ import print_function
# In[3]:
dataset = pd.read_csv("csv/enjoy_baseball/result.csv")
# In[4]:
dataset.head()
# In[5]:
def ip_to_real(x):
    #最初の４文字を取り出せば、年になる
    return float(eval(x))
dataset["HOME_K/9"] = dataset["HOME_K"] * 9 / dataset["HOME_IP"].apply(ip_to_real)
dataset["HOME_BB/9"] = dataset["HOME_BB"] * 9 / dataset["HOME_IP"].apply(ip_to_real)
dataset["HOME_K/BB"] = dataset["HOME_K"] / dataset["HOME_BB"]
dataset["VISITOR_K/9"] = dataset["VISITOR_K"] * 9 / dataset["VISITOR_IP"].apply(ip_to_real)
dataset["VISITOR_BB/9"] = dataset["VISITOR_BB"] * 9 / dataset["VISITOR_IP"].apply(ip_to_real)
dataset["VISITOR_K/BB"] = dataset["VISITOR_K"] / dataset["VISITOR_BB"]
dataset["HOME_K/BB / VISITOR_K/BB"] = dataset["HOME_K/BB"] / dataset["VISITOR_K/BB"]
# In[6]:
dataset[dataset["HOME_K/BB / VISITOR_K/BB"] < 1].sort_values(by=["Team", "Year"], ascending=True)
# In[7]:
dataset[dataset["Team"] == 'Fighters'][["Year" ,"Team", "HOME_K/BB", "VISITOR_K/BB", "HOME_K/BB / VISITOR_K/BB"]]
# In[8]:
dataset[dataset["HOME_K/BB / VISITOR_K/BB"] > 1.2].sort_values(by=["Team", "Year"], ascending=True)
# In[15]:
dataset[["Year", "Team", "HOME_K/BB"]].sort_values(by=["HOME_K/BB"], ascending=False)