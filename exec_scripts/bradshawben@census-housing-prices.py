#!/usr/bin/env python
# coding: utf-8
# In[33]:
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from warnings import filterwarnings
filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')
# In[7]:
def read_housing_data(p):
    return pd.read_csv(p, encoding='latin1')
raw = read_housing_data('housing.csv')
raw.head(5)
# In[10]:
raw.info()
# In[14]:
raw.describe()
# In[18]:
raw.hist(bins=50, figsize=(15,20))
plt.show()
# In[39]:
def test_train_split(df, test_proportion):
    df['is_train'] = np.random.rand(df.shape[0])
    df['is_train'] = df['is_train'].map(lambda x: x < test_proportion)
    test, train = df[df['is_train'] == False], df[df['is_train'] == True]
    test.drop('is_train', axis=1, inplace=True)
    train.drop('is_train', axis=1, inplace=True)
    return test, train
test, train = test_train_split(raw, 0.8)
train.head(5)