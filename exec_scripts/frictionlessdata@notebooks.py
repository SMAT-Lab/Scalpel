#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().system('ls -l')
# In[2]:
get_ipython().system('cat pipeline-spec.yaml')
# In[3]:
get_ipython().system('dpp')
# In[4]:
get_ipython().system('dpp run ./worldbank-co2-emissions')
# In[5]:
get_ipython().system('ls -l')
# In[6]:
get_ipython().system('ls -l co2-emisonss-wb/')
# In[7]:
get_ipython().run_line_magic('cat', 'co2-emisonss-wb/datapackage.json | json_pp')
# In[8]:
get_ipython().system('head co2-emisonss-wb/data/global-data.csv')