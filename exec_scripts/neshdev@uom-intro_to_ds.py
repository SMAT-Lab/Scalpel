#!/usr/bin/env python
# coding: utf-8
# In[120]:
import pandas as pd
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)
names_ids = df.index.str.split('\s\(') # split the index by '('
df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)
df = df.drop('Totals')
df.head()
# In[122]:
# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]
# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 
# In[123]:
def answer_one():
    return df['Gold'].argmax()
answer_one()
# In[149]:
def answer_two():
    diff = df['Gold'] - df['Gold.1']
    return diff.argmax()
answer_two()
# In[169]:
def answer_three():
    copy =  df.where((df['Gold'] > 0) & (df['Gold.1'] > 0)).dropna()
    total_golds = copy['Gold'] + copy['Gold.1']
    relative_diff = abs(copy['Gold'] - copy['Gold.1']) / total_golds
    return relative_diff.argmax()
answer_three()
# In[230]:
def answer_four():
    df['Points'] = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']*1
    return df['Points']
answer_four()
# In[691]:
census_df = pd.read_csv('census.csv')
census_df.head()
# In[425]:
def answer_five():
    idx = census_df.groupby('STATE').size().argmax()
    states = census_df[['STATE','STNAME']].drop_duplicates()
    states = states.set_index('STATE')
    return states.loc[idx]['STNAME']
answer_five()
# In[850]:
def answer_six():
    states = census_df.copy()
    states = states[['STATE','STNAME']].drop_duplicates()
    states = states.set_index('STATE')
    copy = census_df.copy()
    copy = copy[copy.SUMLEV == 50]
    columns_to_keep = ['STATE',
                       'COUNTY',
                       'POPESTIMATE2015']
    copy = copy[columns_to_keep]
    top3_populous_counties_by_state = copy.sort_values(['STATE','POPESTIMATE2015'],ascending = [True,False]).groupby(['STATE']).head(3)
    top3_populous_counties_by_state = top3_populous_counties_by_state.groupby('STATE').POPESTIMATE2015.sum()
    top3 = top3_populous_counties_by_state.sort_values(ascending=False).head(3).index.values
    return list(states.loc[top3].STNAME)
answer_six()
# In[793]:
def answer_seven():
    c = census_df.copy()
    c = c.set_index('CTYNAME')
    c = c[c.SUMLEV != 40]
    c['max_delta'] = c[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']].max(axis=1)
    c['min_delta'] = c[['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']].min(axis=1)
    c['diff_delta'] = abs(c.max_delta - c.min_delta)
    c.sort_values(['diff_delta'], ascending=False, inplace=True)
    return c['diff_delta'].argmax()
answer_seven()
# In[677]:
def answer_eight():
    copy = census_df
    copy = copy[(copy.REGION == 1) | (copy.REGION == 2)]
    copy = copy[copy.CTYNAME.str.contains('Washington')]
    copy = copy[(copy.POPESTIMATE2015 > copy.POPESTIMATE2014)]
    return copy[['STNAME', 'CTYNAME']]
answer_eight()