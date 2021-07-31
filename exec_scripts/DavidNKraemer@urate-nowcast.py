#!/usr/bin/env python
# coding: utf-8
# In[198]:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as st
from statsmodels.tsa.arima_model import ARMA
import statsmodels.graphics.tsaplots as stsa
# In[14]:
get_ipython().run_line_magic('matplotlib', 'inline')
# In[43]:
sns.set_context('talk')
sns.set_style('white')
# In[131]:
data = np.random.randn(10000,2)
plt.plot(np.cumsum(data[:,0]), np.cumsum(data[:,1]), '--', alpha=0.3)
sns.despine()
# In[209]:
st_date = pd.Timestamp('2015-01-01')
ed_date = pd.Timestamp('2017-01-01')
unrate = pd.read_csv('../data/UNRATE.csv', index_col=0)
unrate.index = pd.to_datetime(unrate.index)
model = ARMA(unrate.diff()[-100:], (1,0), freq='MS')
results = model.fit()
unrate['FORECAST'] = results.predict(start=st_date, end=ed_date, dynamic=False)
plt.plot(pd.date_range(st_date, ed_date, freq='MS'), unrate['UNRATE'][st_date] + unrate['FORECAST'].dropna())
plt.plot(unrate.index[-50:], unrate['UNRATE'][-50:])
sns.despine()
# In[206]:
stsa.plot_acf(unrate['UNRATE'].diff())
# In[210]:
results.summary()