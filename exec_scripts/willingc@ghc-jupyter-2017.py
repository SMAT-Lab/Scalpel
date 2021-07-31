#!/usr/bin/env python
# coding: utf-8
# In[37]:
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import seaborn as sns
sns.set_style("whitegrid")
from matplotlib import pyplot as plt
# In[10]:
infantMortality = pd.read_csv("OSD_BDChildData.csv")
# In[11]:
infantMortality
# In[38]:
cs=sns.color_palette("cubehelix", 10)
# In[73]:
import pprint as pp
def plotdat(l, title_text='Infant mortality rate in Bangladesh', sortON=True, plot_type="line"):
    if sortON == True:
        l.sort_values(inplace=True)
    fig=plt.figure(figsize=(10,5))
    plt.yticks(fontsize=8)
    
    
    if plot_type=="line":
        l.plot(kind=plot_type, fontsize=12,color = cs[1], marker='o')
    else:
        l.plot(kind=plot_type, fontsize=12,color = cs[1])
    
    plt.xlabel('')
    plt.ylabel('Infant mortality rate',fontsize=10)
    plt.title(title_text, fontsize=20)
# In[16]:
infantMortality.plot()
# In[20]:
infantMortality.columns
# In[72]:
infantMortality1 = infantMortality[infantMortality['YEAR (DISPLAY)'] >= 2000]
# infant_head = infantMortality1.head(1)
reduced = infantMortality1[["YEAR (DISPLAY)", "Numeric"]]
print(reduced)
l = reduced.groupby('YEAR (DISPLAY)')['Numeric']
# In[31]:
infantMortality1.head()
# In[75]:
plt.scatter(reduced['YEAR (DISPLAY)'],reduced['Numeric'])
plt.xlabel('Year')
plt.ylabel('percentage',fontsize=10)
plt.title('Infant Mortality Rate in Bangladesh', fontsize=20)