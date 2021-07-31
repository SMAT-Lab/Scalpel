#!/usr/bin/env python
# coding: utf-8
# In[2]:
import matplotlib.pyplot as plt
import numpy as np
import seaborn
import pandas as pd
from pandas import DataFrame, Series
get_ipython().run_line_magic('matplotlib', 'inline')
# In[3]:
batting_data = pd.read_csv('Data/core/Batting.csv', sep = ",", dtype = str).fillna(0)
# In[4]:
batting_data = batting_data[['playerID', 'yearID', 'H', 'BB', 'HBP', 'AB', 'SF']]
# In[5]:
batting_data.head()
# In[6]:
salary_data = pd.read_csv('Data/core/Salaries.csv', sep = ",", dtype = str).fillna(0)
# In[7]:
salary_data = salary_data[['playerID', 'salary']]
# In[8]:
salary_data.head()
# In[9]:
fielding_data = pd.read_csv('Data/core/Fielding.csv', sep = ",", dtype = str).fillna(0)
# In[10]:
fielding_data = fielding_data[['playerID', 'POS']]
# In[11]:
fielding_data.head()
# In[12]:
batting_and_salary = pd.merge(batting_data, salary_data)
# In[13]:
batting_and_salary.head()
# In[14]:
batting_and_salary.sort_values('playerID')
# In[15]:
amalgamated_data = pd.merge(batting_and_salary, fielding_data)
# In[16]:
amalgamated_data.head()
# In[17]:
amalgamated_data.sort_values('playerID')
# In[18]:
# relevant_data = amalgamated_data[['playerID', 'yearID', 'AB', 'H', 'BB', 'HBP', 'SF', 'salary', 'POS']]
# In[19]:
# relevant_data.head()
# In[20]:
float_data = amalgamated_data[['yearID', 'AB', 'H', 'BB', 'HBP', 'SF', 'salary']].astype(float)
# In[21]:
amalgamated_data.pop('yearID')
# In[22]:
amalgamated_data.pop('salary')
# In[23]:
cleaned_data = pd.concat([amalgamated_data, float_data], axis = 1)
# In[24]:
cleaned_data.head()
# In[25]:
len(cleaned_data)
# In[26]:
amalgamated_data = cleaned_data
# In[27]:
amalgamated_data.head()
# In[28]:
top_list = ['H', 'BB', 'HBP']
# In[29]:
bottom_list = ['AB', 'BB' , 'HBP', "SF"]
# In[30]:
amalgamated_data['OBP'] = amalgamated_data[top_list].sum(axis=1) / amalgamated_data[bottom_list].sum(axis=1)
# In[31]:
amalgamated_data.fillna(0)
# In[32]:
# def get_obp(hits, walks, hit_by_pitch, at_bats, sacrifice_flies):
#     return ((hits + walks + hit_by_pitch)/(at_bats + walks + hit_by_pitch + sacrifice_flies))
# In[33]:
# amalgamated_data['OBP'] = get_obp(cleaned_data['H'], cleaned_data['BB'], cleaned_data['HBP'], cleaned_data['AB'], cleaned_data['SF'])
# In[34]:
amalgamated_data = amalgamated_data.fillna(0)
# In[35]:
amalgamated_data.head()
# In[36]:
amalgamated_data = amalgamated_data.drop(amalgamated_data[amalgamated_data.OBP == 1].index)
# In[37]:
amalgamated_data.head()
# In[38]:
len(amalgamated_data)
# In[39]:
amalgamated_data = amalgamated_data.drop(amalgamated_data[amalgamated_data.OBP == 0].index)
# In[40]:
amalgamated_data.head()
# In[41]:
len(amalgamated_data)
# In[42]:
amalgamated_data.head()
# In[43]:
amalgamated_data = amalgamated_data.drop(amalgamated_data[amalgamated_data.yearID < 2014].index)
# In[44]:
amalgamated_data = amalgamated_data.drop_duplicates('playerID')
# In[45]:
len(amalgamated_data)
# In[46]:
amalgamated_data.head()
# In[47]:
type(amalgamated_data['OBP'])
# In[55]:
amalgamated_data['OBP_per_dollar'] = amalgamated_data['OBP'] / amalgamated_data['salary']
# In[56]:
amalgamated_data.head()
# In[57]:
amalgamated_data.sort_values(by='OBP_per_dollar', ascending=False)
# In[59]:
final_data_set = amalgamated_data[['playerID', 'POS', 'yearID', 'salary', 'OBP', 'OBP_per_dollar']]
# In[64]:
final_data_set.sort_values(by='OBP_per_dollar', ascending=False)