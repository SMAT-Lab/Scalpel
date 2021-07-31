#!/usr/bin/env python
# coding: utf-8
# In[1]:
RAW_DATA_DIR = '../data/raw'
PROCESSED_DATA_FILENAME = '../data/processed/ufo_alcohol.csv'
UFO_SIGHTINGS = RAW_DATA_DIR + '/ufo-scrubbed-geocoded-time-standardized.csv'
ALC_CONSUMPTION = RAW_DATA_DIR + '/DP_LIVE_22032018202902423.csv'
# In[2]:
import pandas as pd
from IPython.display import display
# In[3]:
dateparse = lambda date: pd.datetime.strptime(date.replace('24:', '00:'), '%m/%d/%Y %H:%M')
ufo_df = pd.read_csv(UFO_SIGHTINGS, header=None, low_memory=False, 
                 parse_dates=['datetime'], date_parser=dateparse,
                 names=['datetime', 'city', 'state', 'country','shape',
                        'duration (seconds)','duration (hours/min)',
                        'comments','date posted','latitude','longitude'])
# In[4]:
ufo_df = ufo_df.loc[ufo_df['country'] == 'us']
# In[5]:
display(ufo_df.head())
# In[6]:
ufo_df['year'] = ufo_df['datetime'].dt.year
# In[7]:
ufo_df = ufo_df [['year']]
# In[8]:
original = ufo_df.copy()
ufo_df = pd.DataFrame({'ufo_sightings' : original.groupby( [ 'year'] )['year'].count()}).reset_index()
# In[9]:
display(ufo_df.tail())
# In[10]:
ufo_df.describe(include='all').T
# In[11]:
alc_df = pd.read_csv(ALC_CONSUMPTION, low_memory=False)
# In[12]:
display(alc_df.head())
# In[13]:
alc_df = alc_df.loc[alc_df['LOCATION'] == 'USA']
# In[14]:
alc_df = alc_df [['TIME', 'Value']]
# In[15]:
alc_df = alc_df.rename(columns={'TIME': 'year', 'Value': 'alcohol_consumption'})
# In[16]:
display(alc_df.head())
# In[17]:
alc_df.describe(include='all').T
# In[18]:
merged_df = pd.merge(ufo_df, alc_df, on='year')
# In[19]:
display(merged_df.head())
# In[20]:
merged_df.to_csv(PROCESSED_DATA_FILENAME, sep=',', index=False)