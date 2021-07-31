#!/usr/bin/env python
# coding: utf-8
# In[2]:
import pandas as pd
import numpy as np
# In[2]:
np.random.binomial(1, 0.5)
# In[3]:
np.random.binomial(1000, 0.5)/1000
# In[4]:
chance_of_tornado = 0.01/100
np.random.binomial(100000, chance_of_tornado)
# In[5]:
chance_of_tornado = 0.01
tornado_events = np.random.binomial(1, chance_of_tornado, 1000000)
    
two_days_in_a_row = 0
for j in range(1,len(tornado_events)-1):
    if tornado_events[j]==1 and tornado_events[j-1]==1:
        two_days_in_a_row+=1
print('{} tornadoes back to back in {} years'.format(two_days_in_a_row, 1000000/365))
# In[6]:
np.random.uniform(0, 1)
# In[16]:
np.random.normal(0.75)
# In[44]:
distribution = np.random.normal(0.75,size=1000)
np.sqrt(np.sum((np.mean(distribution)-distribution)**2)/len(distribution))
# In[32]:
np.std(distribution)
# In[33]:
import scipy.stats as stats
stats.kurtosis(distribution)
# In[34]:
stats.skew(distribution)
# In[35]:
chi_squared_df2 = np.random.chisquare(2, size=10000)
stats.skew(chi_squared_df2)
# In[36]:
chi_squared_df5 = np.random.chisquare(5, size=10000)
stats.skew(chi_squared_df5)
# In[45]:
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
output = plt.hist([chi_squared_df2,chi_squared_df5], bins=50, histtype='step', 
                  label=['2 degrees of freedom','5 degrees of freedom'])
plt.legend(loc='upper right')
# In[3]:
df = pd.read_csv('grades.csv')
# In[4]:
df.head()
# In[5]:
len(df)
# In[6]:
early = df[df['assignment1_submission'] <= '2015-12-31']
late = df[df['assignment1_submission'] > '2015-12-31']
# In[50]:
early.mean()
# In[51]:
late.mean()
# In[52]:
from scipy import stats
get_ipython().run_line_magic('pinfo', 'stats.ttest_ind')
# In[53]:
stats.ttest_ind(early['assignment1_grade'], late['assignment1_grade'])
# In[54]:
stats.ttest_ind(early['assignment2_grade'], late['assignment2_grade'])
# In[55]:
stats.ttest_ind(early['assignment3_grade'], late['assignment3_grade'])