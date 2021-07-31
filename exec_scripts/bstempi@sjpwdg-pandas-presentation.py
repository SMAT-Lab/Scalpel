#!/usr/bin/env python
# coding: utf-8
# In[1]:
rows = [
['Aberdeen Township', 18150, 19, 0, 13, 6],
['Absecon', 8380, 21, 0, 4, 15],
['Allendale', 6712, 0, 0, 0, 0],
['Allenhurst', 493, 0, 0, 0, 0],
['Allentown', 1812, 3, 0, 0, 3],
['Alpine', 2314, 1, 0, 0, 1],
['Andover Township', 6273, 1, 0, 0, 1],
]
# In[2]:
import pandas as pd
df = pd.DataFrame.from_records(rows, columns=['City', 'Population', 'Violent Crimes', 'Murders', 'Roberies', 'Aggrevated Assaults'])
# In[3]:
df
# In[4]:
# Q1 
sum_people = 0
sum_violent_crimes = 0
for row in rows:
	sum_people += row[1]
	sum_violent_crimes += row[2]
	
violent_crimes_ratio = sum_violent_crimes / sum_people
violent_crimes_per_thousand_people = violent_crimes_ratio * 1000
# Q2
sum_aggrevated_assaults = 0
sum_violent_crimes = 0
for row in rows:
	sum_aggrevated_assaults += row[5]
	sum_violent_crimes += row[2]
	
aggrevated_assault_ratio = sum_aggrevated_assaults / sum_violent_crimes
# Q3
violent_crimes_per_1k_people_per_city = list()
for row in rows:
	result_row = [row[0], 1000 * row[2] / row[1]]
	violent_crimes_per_1k_people_per_city.append(result_row)
violent_crimes_per_thousand_people, aggrevated_assault_ratio, violent_crimes_per_1k_people_per_city
# In[5]:
# Q1
violent_crimes_per_thousand_people = 1000 * df['Violent Crimes'].sum() / df['Population'].sum()
# Q2
aggrevated_assault_ratio = df['Aggrevated Assaults'].sum() / df['Violent Crimes'].sum()
# Q3
stats_per_city = df.groupby('City').sum()
stats_per_city['Violent Crimes Per 1000'] = 1000 * stats_per_city['Violent Crimes'] / stats_per_city['Population']
violent_crimes_per_thousand_people, aggrevated_assault_ratio, stats_per_city[['Violent Crimes Per 1000']]
# In[6]:
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
stats_per_city.plot(y='Violent Crimes Per 1000', kind='bar')