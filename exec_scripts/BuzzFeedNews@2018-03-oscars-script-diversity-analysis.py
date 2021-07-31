#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import os
from glob import glob
import numpy as np
# In[2]:
actors = pd.read_csv("../data/actor-metrics.csv")
actors.head()
# In[3]:
def single_group(col):
    """
    Groups on one col 
    Sums sentences and words
    Calcs percents of columns against whole
    Returns data frame
    """
    return actors.groupby(col).agg({
        "sentences": np.sum, # sum number of sentences
        "words": np.sum, # sum number of words
        "actor": "count"
    }).assign(
        percent_sentences = lambda frame: ( frame['sentences'] / frame['sentences'].sum() ) * 100,
        percent_words = lambda frame: ( frame['words'] / frame['words'].sum()) * 100,
        percent_actor = lambda frame: ( 
            (frame["actor"] / frame['actor'].sum()) * 100
        ) 
    )
# In[4]:
def double_group(col1, col2):
    """
    Groups on two cols 
    Counts actors and percent for race or gender 
    Calcs percents of columns against whole
    Returns data frame
    """
    
    grouped = actors.groupby([col1, col2]).agg({
        "actor": "count"
        # unstack to remove multindex
    }).unstack() \
    .fillna(0).astype(int)
    # drop the extra multi column
    grouped.columns = grouped.columns.get_level_values(1)
    # create new col for total
    if col2 == "gender":
        grouped['total'] = grouped['male'] + grouped['female']
        # make percent cols
        grouped['female_percent'] = (grouped['female'] / grouped['total'] ) * 100
        grouped['male_percent'] = ( grouped['male'] / grouped['total']) * 100
    elif col2 == "race_simple":
        # make a total column
        grouped['total'] = grouped['POC'] + grouped['White']
        # make a percent column
        grouped['white_percent'] = (grouped['White'] / grouped['total'] ) * 100
        grouped['poc_percent'] = ( grouped['POC'] / grouped['total']) * 100
    # remove the column's namne
    grouped.columns.name = ""
    # display
    return grouped
# In[5]:
def double_word_group(unit, col1, col2):
    """
    Takes words/sentences as "unit" and two arbitrary columns
    """
    # group by year and gender
    bycols = actors.groupby([col1, col2]).agg({
        unit: np.sum,
    }).unstack() \
    .fillna(0).astype(int)
    # drop the extra multi column
    bycols.columns = bycols.columns.droplevel()
    # math:
    if col2 == "gender":
        bycols['total_{}'.format(unit)] = bycols['female'] + bycols['male']
        # make a percent column
        bycols['female_percent'] = (bycols['female'] / bycols['total_{0}'.format(unit)] ) * 100
        bycols['male_percent'] = ( bycols['male'] / bycols['total_{0}'.format(unit)]) * 100
    elif col2 == "race_simple":
        
        bycols['total_{0}'.format(unit)] = bycols['POC'] + bycols['White']
        # make a percent column
        bycols['white_percent'] = (bycols['White'] / bycols['total_{0}'.format(unit)] ) * 100
        bycols['poc_percent'] = ( bycols['POC'] / bycols['total_{0}'.format(unit)]) * 100
        
    # clean up the column
    bycols.columns.name = ""
    # display last three columns for clarity
    return bycols.iloc[:, 2:]
# In[6]:
single_group('gender')
# In[7]:
single_group('race')
# In[8]:
single_group('race_simple')
# In[9]:
double_group('year', 'gender')
# In[10]:
double_group('year', 'race_simple')
# In[11]:
double_word_group('sentences', 'year', 'gender')
# In[12]:
double_word_group('words', 'year', 'gender')
# In[13]:
double_word_group('sentences', 'year', 'race_simple')
# In[14]:
double_word_group('words', 'year', 'race_simple')
# In[15]:
double_group('film', 'race_simple').sort_values("poc_percent", ascending = False)
# In[16]:
double_group('film', 'gender').sort_values(
    "female_percent", ascending = False
)
# In[17]:
double_word_group("words", "film", "gender").sort_values(
    by = "female_percent",
    ascending = False
)
# In[18]:
double_word_group("sentences", "film", "gender").sort_values(
    by = "female_percent",
    ascending = False
)
# In[19]:
double_word_group("sentences", "film", "race_simple").sort_values(
    by = "poc_percent",
    ascending = False
)
# In[20]:
double_word_group("words", "film", "race_simple").sort_values(
    by = "poc_percent",
    ascending = False
)