#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import atus_analysis as at
get_ipython().run_line_magic('matplotlib', 'inline')
# In[2]:
activity, respondent, roster = at.read_in_data()
# In[3]:
child_care = activity[['TUCASEID', 'TUACTIVITY_N', 'TUACTDUR24']].copy()
activity_codes = at.get_codes(activity) # This is re-used below in the Sleep code.
child_care['codes'] = activity_codes
child_care_by_ID = child_care.groupby(['TUCASEID'])
child_care_codes = ['0301', '0302', '0303']
child_care_time = pd.Series(at.get_minutes_subject(child_care_by_ID, child_care_codes), name='Child Care Time')
weight = respondent[['TUCASEID', 'TUFINLWGT', 'TRCHILDNUM', 'TRERNWA']].copy()
weight.set_index(weight.pop('TUCASEID'), inplace=True)
weighted_child_care = weight.join(child_care_time)
weighted_child_care['TRERNWA'] = weighted_child_care['TRERNWA'].replace(-1, 0)
weighted_child_care['TRERNWA'] = weighted_child_care['TRERNWA'] / 100
weighted_child_care['Weighted Care Time'] = weighted_child_care['TUFINLWGT'] * weighted_child_care['Child Care Time']
weighted_child_care = weighted_child_care.rename(columns={'TUFINLWGT': 'Weight',
                                                'TRCHILDNUM': 'Number of Children',
                                                'TRERNWA': 'Weekly Income'})
# In[4]:
summed_child_care = weighted_child_care.sum()
child_care_avg_daily_minutes = summed_child_care['Weighted Care Time'] / summed_child_care['Weight']
child_care_hourly = child_care_avg_daily_minutes / 60
# In[5]:
child_care_hourly
# In[6]:
weighted_child_care.plot(kind='scatter', x='Number of Children', y='Child Care Time')
# In[7]:
sns.jointplot(x="Number of Children", y='Child Care Time', data=weighted_child_care)
# In[8]:
sns.FacetGrid(weighted_child_care, hue="Number of Children", size=8)    .map(plt.scatter, "Child Care Time", "Weekly Income")    .add_legend()
# In[9]:
weighted_child_care.corr()
# In[10]:
sleep = activity[['TUCASEID', 'TUACTIVITY_N', 'TUACTDUR24']].copy()
sleep['codes'] = activity_codes
sleep_by_ID = sleep.groupby(['TUCASEID'])
sleep_codes = ['010101', '010103']
sleeping_time = pd.Series(at.get_minutes_subject(sleep_by_ID, sleep_codes), name='Minutes Sleeping')
sleep_weight = respondent[['TUCASEID', 'TUFINLWGT', 'TRCHILDNUM', 'TRERNWA']].copy()
age_sex = pd.DataFrame.from_records([(row.TUCASEID, row.TEAGE, row.TESEX) for row in roster.itertuples() if row.TULINENO == 1], columns=['TUCASEID', 'Age', 'Sex'])
sleep_weight.set_index(sleep_weight.pop('TUCASEID'), inplace=True)
age_sex.set_index(age_sex.pop('TUCASEID'), inplace=True)
weighted_sleep = sleep_weight.join([age_sex, sleeping_time])
weighted_sleep['Weighted Minutes Sleeping'] = weighted_sleep['TUFINLWGT'] * weighted_sleep['Minutes Sleeping']
weighted_sleep['TRERNWA'] = weighted_sleep['TRERNWA'].replace(-1, 0)
weighted_sleep['TRERNWA'] = weighted_sleep['TRERNWA'] / 100
weighted_sleep['Sex'] = ['Male' if cell == 1 else 'Female' for cell in weighted_sleep['Sex']]
weighted_sleep = weighted_sleep.rename(columns={'TUFINLWGT': 'Weight',
                                                'TRCHILDNUM': 'Number of Children',
                                                'TRERNWA': 'Weekly Income'})
# In[11]:
summed_sleep = weighted_sleep.sum()
average_sleep_minutes = summed_sleep['Weighted Minutes Sleeping'] / summed_sleep['Weight']
average_sleep_hour = average_sleep_minutes / 60
# In[12]:
average_sleep_hour
# In[13]:
weighted_sleep.plot(kind='scatter', x='Age', y='Minutes Sleeping')
# In[14]:
sns.jointplot(x='Number of Children', y='Minutes Sleeping', data=weighted_sleep)
# In[17]:
sns.FacetGrid(weighted_sleep, hue="Sex", size=8)    .map(plt.scatter, "Age", "Minutes Sleeping")    .add_legend()
# In[16]:
weighted_sleep.corr()