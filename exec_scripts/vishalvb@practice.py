#!/usr/bin/env python
# coding: utf-8
# In[1]:
from matplotlib import pyplot as plt
import pandas as pd
# In[2]:
data = pd.read_csv('countries.csv')
data.head()
# In[5]:
data_us = data[data.country == 'United States']
data_us.head()
# In[7]:
plt.plot(data_us.year, data_us.gdpPerCapita)
plt.xlabel('year')
plt.ylabel('GDP Per Captia')
plt.title('US GSP per captia')
plt.show()
# In[8]:
data_china = data[data.country == 'China']
data_china.head()
# In[9]:
plt.plot(data_china.year, data_china.gdpPerCapita)
plt.xlabel('year')
plt.ylabel('GDP Per Captia')
plt.title('CHINA GSP per captia')
plt.show()
# In[11]:
plt.plot(data_china.year, data_china.gdpPerCapita)
plt.plot(data_us.year, data_us.gdpPerCapita)
plt.xlabel('Year')
plt.ylabel('GPD Per Capita')
plt.legend(['China', 'USA'])
plt.show()
# In[19]:
us_growth = (data_us.gdpPerCapita / data_us.gdpPerCapita.iloc[0]  ) * 100 #iloc allows to select with interger location
# In[20]:
china_growth = (data_china.gdpPerCapita / data_china.gdpPerCapita.iloc[0]  ) * 100
# In[21]:
plt.plot(data_china.year, china_growth)
plt.plot(data_us.year, us_growth)
plt.xlabel('Year')
plt.ylabel('GPD Per Capita')
plt.legend(['China', 'USA'])
plt.show()
# In[24]:
us_population = (data_us.population / data_us.population.iloc[0]) * 100
# In[25]:
us_population
# In[26]:
china_population = (data_china.population / data_china.population.iloc[0]) * 100
china_population
# In[27]:
plt.plot(data_china.year, china_population)
plt.plot(data_us.year, us_population)
plt.xlabel('Year')
plt.ylabel('Popuation growth')
plt.legend(['China', 'USA'])
plt.show()