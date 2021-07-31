#!/usr/bin/env python
# coding: utf-8
# In[1]:
import os, sys, requests, json
import pandas as pd
import numpy as np
from numpy.random import randint
import matplotlib.pyplot as plt
np.random.seed(123)
# In[2]:
domain = 'http://www.omdbapi.com/?apikey='
query = '&i='
api_key = '98b8e0fb'
code = 'tt'
# In[12]:
id_collected = []
start_id = 1100000
len_id = 100
def gen_id(start_id,len_id):
    '''Generates a variable list of all collected imdb IDs depending on start and length'''
    for num in range(len_id):
        imdb_ord = start_id + num
        imdb_id = code + str(imdb_ord)
        id_collected.append(imdb_id)
    return id_collected
    
total_list =[]
throw_away =[]
series_list =[]
def get_series(api_key):
    '''This function will take the queries as inputs and churn out the JSON data'''
    try:
        global domain
        for series in gen_id(start_id, len_id): 
            url = domain + api_key + query + series
            response = requests.get(url).json()
            data_dict = dict(response)
            total_list.append(data_dict)
    except:
        pass
    return total_list
# In[9]:
total_list = get_series(api_key)
def get_sublists(film_type):
    '''This function acts as a boolean condition for whatever movies you want to keep from that long list'''
    for film in total_list:
        if film['Response'] == 'True':
            if film['Type'] == film_type:
                series_list.append(film)
        else:
            del film             
    return series_list
# In[10]:
#Quick check to make sure above function is working properly
for film in get_sublists('movie'):
    print('%s is a %s' % (film['Title'],film['Type']))
# In[11]:
#At this point in time, manipulation of data really depends on the nature of the hypothesis
#Here i chose to extract and examine the relationship between IMDb's score and year of release with a small subset
criteria = ['Title','Year','imdbRating']
df = []
for film in get_sublists('movie'):
    rows = (film[criteria[0]],film[criteria[1]],film[criteria[2]])
    df.append(rows)
final = pd.DataFrame(df)
final.columns = criteria
final = final.drop_duplicates().replace('N/A',np.nan).dropna(how='any')
final