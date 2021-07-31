#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import statsmodels.api as sm
# In[2]:
df = pd.read_csv('../data/ces2013.csv')
# In[3]:
df = df[df.FDHO > 0] # filter FDHO > 0
# In[4]:
results = sm.OLS(df.FDHO, sm.add_constant(df.EXP)).fit()
# In[5]:
results.summary()
# In[6]:
results.params
# In[23]:
coefficients = dict()
for col in df.columns:
    df_tmp = df[df[col] > 0]
    results = sm.OLS(df_tmp[col], sm.add_constant(df_tmp.EXP)).fit()
    print('{}: n={}, coeff={}, r^2={}'.format(col, results.nobs, results.params[1], results.rsquared))
    coefficients[results.params[1]] = (col, results.nobs)
# In[32]:
for c in sorted(coefficients, reverse=True):
    col, n = coefficients[c]
    print(col, round(c, 4), '{0: .1f}%'.format(n / len(df) * 100))