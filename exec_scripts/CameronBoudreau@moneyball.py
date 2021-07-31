#!/usr/bin/env python
# coding: utf-8
# In[383]:
get_ipython().run_line_magic('matplotlib', 'inline')
import re
import pandas as pd
import matplotlib as plt
import numpy as np
# In[384]:
master = pd.read_csv("data/Master.csv", sep=",")
master = master[["playerID", "nameFirst", "nameLast", "finalGame"]]
master.sort_values('playerID').head(10)
# In[385]:
batting = pd.read_csv("data/Batting.csv", sep=",")
batting = batting[["playerID", "H", "BB", "HBP", "AB", "SF"]]
mean_batting = batting.sort_values('playerID').groupby('playerID').mean()
mean_batting.fillna(value=0)
mean_batting.reset_index(level=0, inplace=True)
mean_batting.head(10)
# In[386]:
salaries = pd.read_csv("data/Salaries.csv", sep=",")
salaries = salaries[["playerID", "yearID", 'salary']]
salaries = salaries.sort_values(['playerID', 'yearID']).drop_duplicates('playerID', keep='last')
salaries = salaries[['playerID', 'salary']]
salaries.head(10)
# In[387]:
fielding = pd.read_csv("data/FieldingPost.csv", sep=",")
fielding = fielding.sort_values(['playerID', 'yearID'])
fielding = fielding.drop_duplicates('playerID', keep='last')
fielding = fielding[['playerID', 'POS']].copy()
fielding.sort_values('playerID')
# In[388]:
master_list = master.merge(mean_batting)
master_list = pd.merge(master_list, salaries)
master_list = pd.merge(master_list, fielding)
master_list.head(10)
# In[389]:
only_2015 = master_list[(pd.to_datetime(master_list['finalGame'], format='%Y-%m-%d').dt.year == 2015) | master_list['finalGame'].isnull()].copy()
only_2015
# In[390]:
def get_obp(H, AB, BB, SF, HBP=0):
    return ((H+BB+HBP)/(AB+BB+HBP+SF))
# In[391]:
only_2015['OBP'] = get_obp(only_2015['H'], only_2015['AB'], only_2015['BB'], only_2015['SF'], only_2015['HBP'])
# In[392]:
clean_2015 = only_2015[(only_2015.OBP != 0) & (only_2015.OBP != 1) & (only_2015.OBP != None) & (only_2015.OBP.notnull())]
# In[393]:
clean_2015.head(10)
# In[394]:
final_list = clean_2015[['POS', 'OBP', 'salary', 'playerID', 'nameFirst', 'nameLast']].copy()
final_list = final_list.sort_values(['POS', 'OBP'], ascending=False)
final_list.groupby('POS').head()
final_list.head()
# In[397]:
final_list = final_list[(final_list.OBP >= 0.36)]
final_list.sort_values(['POS', 'salary'], ascending=False)
# In[398]:
final_list.sort_values(['POS', 'salary'], ascending=False).drop_duplicates('POS', keep='last')