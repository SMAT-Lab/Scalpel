#!/usr/bin/env python
# coding: utf-8
# In[7]:
import requests
# In[5]:
response = requests.get('http://npr.org')
# In[12]:
response.content
# In[11]:
response.headers