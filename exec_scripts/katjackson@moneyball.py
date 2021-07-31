#!/usr/bin/env python
# coding: utf-8
# In[6]:
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
# In[7]:
master = pd.read_csv('data/core/Master.csv', dtype=str, usecols=['playerID', 'nameGiven', 'deathYear', 'finalGame'])
master.head()
# In[8]:
master = master[pd.isnull(master.deathYear)]
master = master.drop('deathYear', 1)
master.head()
# In[9]:
master['is_inactive'] = master.finalGame[master.finalGame < '2015-01-01']
master = master[pd.notnull(master.is_inactive)]
master = master.drop(['is_inactive', 'finalGame'], 1)
master.head()
# In[10]:
batting = pd.read_csv('data/core/Batting.csv', usecols=['playerID', 'G', 'AB', 'H', 'BB', 'HBP', 'SF'])
batting.head()
# In[11]:
batting = batting.groupby(['playerID']).mean()
batting.head()
# In[12]:
batting = batting.fillna(0)
batting['OBP'] = ((batting.H + batting.BB + batting.HBP)/(batting.AB + batting.BB + batting.HBP + batting.SF))
# In[13]:
batting.sort_values('OBP').head()
# In[14]:
batting = batting[batting.OBP > 0.07]
batting['playerID'] = batting.index
batting.head()
# In[15]:
batting_p = pd.merge(batting, master)
batting_p = batting_p.sort_values('OBP', ascending=False)
# In[16]:
batting_p = batting_p[batting_p['AB'] > 17]
batting_p.head()
# In[17]:
salaries = pd.read_csv('data/core/Salaries.csv')
salaries.head()
# In[18]:
salaries = salaries.groupby('playerID').mean()
salaries = salaries.drop('yearID', 1)
salaries['playerID'] = salaries.index
salaries.head()
# In[19]:
money_ball = pd.merge(batting_p, salaries)
money_ball.head()
# In[20]:
appearances = pd.read_csv('data/core/Appearances.csv')
appearances.head()
x = appearances[appearances['playerID'] == 'abadan01']
x
# In[21]:
appearances = appearances.groupby('playerID').mean()
appearances['G_p'] = appearances.G_p / appearances.G_all
appearances['G_c'] = appearances.G_c / appearances.G_all
appearances['G_1b'] = appearances.G_1b / appearances.G_all
appearances['G_2b'] = appearances.G_2b / appearances.G_all
appearances['G_3b'] = appearances.G_3b / appearances.G_all
appearances['G_ss'] = appearances.G_ss / appearances.G_all
appearances['G_lf'] = appearances.G_lf / appearances.G_all
appearances['G_cf'] = appearances.G_cf / appearances.G_all
appearances['G_rf'] = appearances.G_rf / appearances.G_all
appearances['G_of'] = appearances.G_of / appearances.G_all
appearances = appearances.drop(['yearID', 'G_all', 'GS', 'G_batting', 'G_defense', 'G_dh', 'G_ph', 'G_pr'], 1)
appearances.head()
# In[22]:
first_base = appearances[appearances['G_1b'] > 0.6]
first_base = first_base[['G_1b']]
first_base['playerID'] = first_base.index
first_base = pd.merge(money_ball, first_base)
first_base.head()
# In[23]:
second_base = appearances[appearances['G_2b'] > 0.6]
second_base = second_base[['G_2b']]
second_base['playerID'] = second_base.index
second_base = pd.merge(money_ball, second_base)
second_base.head()
# In[56]:
second_base = second_base[second_base['salary'] < 1000000].sort_values('OBP', ascending=False)
second_base[1:2]
# In[24]:
third_base = appearances[appearances['G_3b'] > 0.6]
third_base = third_base[['G_3b']]
third_base['playerID'] = third_base.index
third_base = pd.merge(money_ball, third_base)
third_base.head()
# In[52]:
third_base = third_base[third_base['salary'] < 1000000].sort_values('OBP', ascending=False)
third_base[:1]
# In[51]:
short_stop = appearances[appearances['G_ss'] > 0.6]
short_stop = short_stop[['G_ss']]
short_stop['playerID'] = short_stop.index
short_stop = pd.merge(money_ball, short_stop)
short_stop.head()
# In[48]:
short_stop = short_stop[short_stop['salary'] < 1000000].sort_values('OBP', ascending=False)
short_stop[:1]
# In[26]:
left = appearances[appearances['G_lf'] > 0.6]
left = left[['G_lf']]
left['playerID'] = left.index
left = pd.merge(money_ball, left)
left.head()
# In[46]:
left = left[left['salary'] < 1000000].sort_values('OBP', ascending=False)
left[:1]
# In[27]:
center = appearances[appearances['G_cf'] > 0.6]
center = center[['G_cf']]
center['playerID'] = center.index
center = pd.merge(money_ball, center)
center.head()
# In[43]:
center = center[center['salary'] < 1000000].sort_values('OBP', ascending=False)
center[:1]
# In[28]:
out = appearances[appearances['G_of'] > 0.6]
out = out[['G_of']]
out['playerID'] = out.index
out = pd.merge(money_ball, out)
out.head()
# In[41]:
out = out[out['salary'] < 1000000].sort_values('OBP', ascending=False)
out[:5]
# In[29]:
pitcher = appearances[appearances['G_p'] > 0.6]
pitcher = pitcher[['G_p']]
pitcher['playerID'] = pitcher.index
pitcher = pd.merge(money_ball, pitcher)
pitcher.head()
# In[38]:
pitcher = pitcher[pitcher['salary'] < 1000000].sort_values('OBP', ascending=False)
pitcher[:1]
# In[30]:
catcher = appearances[appearances['G_c'] > 0.6]
catcher = catcher[['G_c']]
catcher['playerID'] = catcher.index
catcher = pd.merge(money_ball, catcher)
catcher.head()
# In[35]:
catcher = catcher[catcher['salary'] < 1000000].sort_values('OBP', ascending=False)
catcher[:1]