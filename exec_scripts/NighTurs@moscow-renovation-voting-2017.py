#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
import json
import pandas as pd
import numpy as np
import seaborn as sns
from haversine import haversine
# In[2]:
days = [2, 4, 5, 6, 7, 8, 9]
l = []
for i in days:
    with open('../data/renovation_votes_{}0617.json'.format(str(i).rjust(2,'0'))) as file:    
        data = json.load(file)
    for building in data:
        card_fields = building['card_fields']
        l.append({'area_name': card_fields['area_name'],
                  'district_name': card_fields['district_name'],
                  'name': card_fields['name'],
                  'vote_against': card_fields['result']['protiv'],
                  'vote_for': card_fields['result']['za'],
                  'vote_attendance': card_fields['result']['yavka'],
                  'updated_at': card_fields['updated_at'],
                  'center_lat': building['center']['coordinates'][0],
                  'center_lon': building['center']['coordinates'][1]})
df = pd.DataFrame(l)
df['vote_against'] = df.vote_against * 0.01
df['vote_for'] = df.vote_for * 0.01
df['vote_attendance'] = df.vote_attendance * 0.01
df['june_day'] = df.updated_at.apply(lambda x: int(x[:2]))
df.shape
# In[3]:
df.tail()
# In[4]:
dfs = []
for day, nday in zip(days[:-1], days[1:]):
    m = df[df.june_day == day].merge(df[df.june_day == nday], 
                                 on=['name', 'area_name', 'district_name'], 
                                 suffixes=('_day', '_nextday'))
    dfs.append(m[(m.vote_attendance_nextday - m.vote_attendance_day) < 0])
pd.concat(dfs)[['area_name', 
                'district_name', 
                'name', 
                'updated_at_day', 
                'updated_at_nextday',
                'vote_against_day',
                'vote_against_nextday',
                'vote_for_day',
                'vote_for_nextday',
                'vote_attendance_day',
                'vote_attendance_nextday']]    
# In[5]:
against_too_low = []
against_too_high = []
for day, nday in zip(days[:-1], days[1:]):
    m = df[df.june_day == day].merge(df[df.june_day == nday], 
                                 on=['name', 'area_name', 'district_name'], 
                                 suffixes=('_day', '_nextday'))
    m = m[(m.vote_attendance_nextday - m.vote_attendance_day) >= 0.02]
    m['vote_against_low'] = np.floor((m.vote_against_day - 0.01) * 
                                     (m.vote_attendance_day - 0.01) / 
                                     (m.vote_attendance_nextday + 0.01) * 100) / 100
    m['vote_against_high'] = np.ceil(((m.vote_against_day + 0.01) * 
                                      (m.vote_attendance_day + 0.01) + 
                                      (m.vote_attendance_nextday + 0.01) - 
                                      (m.vote_attendance_day - 0.01)) / 
                                      (m.vote_attendance_nextday - 0.01) * 100) / 100
    against_too_low.append(m[m.vote_against_low > m.vote_against_nextday])
    against_too_high.append(m[m.vote_against_high < m.vote_against_nextday])
   
against_too_low = pd.concat(against_too_low)
against_too_low['vote_against_diff'] = m['vote_against_low'] - m['vote_against_nextday']
against_too_high = pd.concat(against_too_high)
against_too_high['vote_against_diff'] = m['vote_against_nextday'] - m['vote_against_high']
columns_to_show = ['area_name', 
                'district_name', 
                'name', 
                'updated_at_day', 
                'updated_at_nextday',
                'vote_against_day',
                'vote_against_nextday',
                'vote_for_day',
                'vote_for_nextday',
                'vote_attendance_day',
                'vote_attendance_nextday', 
                'vote_against_low', 
                'vote_against_high']
against_too_low.sort_values('vote_against_diff', ascending=False)[columns_to_show]
# In[6]:
against_too_high.sort_values('vote_against_diff', ascending=False)[columns_to_show]