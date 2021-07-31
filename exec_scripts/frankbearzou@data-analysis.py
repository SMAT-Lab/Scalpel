#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('ls', '')
# In[2]:
import numpy as np
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# In[3]:
white_house = pd.read_csv("2015_white_house.csv")
# In[4]:
white_house.head(5)
# In[5]:
white_house.shape
# In[6]:
white_house.iloc[0]
# In[7]:
white_house
# In[8]:
plt.hist(white_house["Salary"])
plt.show()
# In[9]:
position_title = white_house["Position Title"]
title_length = position_title.apply(len)
salary = white_house["Salary"]
# In[10]:
from scipy.stats.stats import pearsonr
# In[11]:
pearsonr(title_length, salary)
# In[12]:
plt.scatter(title_length, salary)
plt.xlabel("title length")
plt.ylabel("salary")
plt.title("Title length - Salary Scatter Plot")
plt.show()
# In[13]:
white_house["Salary"].sum()
# In[14]:
max_salary = white_house["Salary"].max()
max_salary_column = white_house["Salary"] == max_salary
white_house.loc[max_salary_column].reset_index(drop = True)
# In[15]:
min_salary = white_house["Salary"].min()
min_salary_column = white_house["Salary"] == min_salary
white_house.loc[min_salary_column].reset_index(drop = True)
# In[16]:
words = {}
for title in position_title:
    title_list = title.split()
    for word in title_list:
        if word not in words:
            words[word] = 1
        else:
            words[word] += 1
# In[17]:
import operator
sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse = True)
# In[18]:
sorted_words