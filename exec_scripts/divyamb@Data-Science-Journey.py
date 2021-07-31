#!/usr/bin/env python
# coding: utf-8
# In[2]:
#importing pandas, matplotlib and numpy packages
import pandas as pd
import matplotlib as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
# In[3]:
#reading in a csv file has become a lot easier since the first project. Now i can use pandas to read it and dont have to write four lines of code
recent_grads = pd.read_csv("recent-grads.csv")
# In[4]:
#location of the first row
recent_grads.iloc[:1]
# In[9]:
#displaying the first two rows to see what data I am dealing with
recent_grads.head(2)
# In[10]:
#last four rows of the dataframa
recent_grads.tail(4)
# In[5]:
#.describe tells me the stats for the entire dataset. This is extremely helpful when I am trying to find differences between two or more columns,for example men and women.
recent_grads.describe()
# In[6]:
raw_data_count = 173
recent_grads = recent_grads.dropna()
# In[7]:
recent_grads.describe()
# In[8]:
cleaned_data_count = 172
# In[9]:
#making sure that there was only one row with missing data
raw_data_count - cleaned_data_count
# In[10]:
#displaying what columns there are in the dataset
recent_grads.columns
# In[11]:
#yay! I finally made a scatterplot with the sample size on the x-axis and Median on the y-axis.
Samplesize_and_median = recent_grads.plot(x="Sample_size",y="Median",kind = "scatter")
Samplesize_and_median.set_title("Samplesize and Median")
# In[12]:
#Some more scatterplots! This time it is to see the correlation between the sample size and the unemployment rate
Samplesize_and_unemploymentrate = recent_grads.plot(x="Sample_size",y="Unemployment_rate",kind = "scatter")
Samplesize_and_unemploymentrate.set_title("Samplesize and Unemployment Rate")
# In[14]:
Fulltime_and_median = recent_grads.plot(x="Full_time",y="Median",kind = "scatter")
Fulltime_and_median.set_title("Full-Time and Median")
# In[15]:
#Scatterplot to seee if women have higher percentages of unemployment or not
Sharewomen_and_unemploymentrate = recent_grads.plot(x="ShareWomen",y="Unemployment_rate",kind = "scatter")
Sharewomen_and_unemploymentrate.set_title("Share-women and Unemployment Rate")
# In[16]:
men_and_median = recent_grads.plot(x="Men",y="Median",kind = "scatter")
men_and_median.set_title("Men and Median")
# In[17]:
women_and_median = recent_grads.plot(x="Women",y="Median",kind = "scatter")
women_and_median.set_title("Women and Median")
# In[26]:
#histograms created for multiple columns. This was to see the freqency of the sample sizes.
recent_grads['Sample_size'].plot(kind='hist')
# In[27]:
recent_grads['Median'].plot(kind='hist')
# In[28]:
recent_grads['Employed'].plot(kind='hist')
# In[29]:
recent_grads['Full_time'].plot(kind='hist')
# In[30]:
recent_grads['ShareWomen'].plot(kind='hist')
# In[31]:
recent_grads['Unemployment_rate'].plot(kind='hist')
# In[32]:
recent_grads['Men'].plot(kind='hist')
# In[33]:
recent_grads['Women'].plot(kind='hist')
# In[34]:
#importing scatter-matrix so I can compare scatterplots and histograms
from pandas.tools.plotting import scatter_matrix
# In[35]:
scatter_matrix(recent_grads[["Sample_size","Men"]],
figsize=(10,10))
# In[36]:
scatter_matrix(recent_grads[["Sample_size","Men","Unemployment_rate"]],
figsize=(10,10))
# In[37]:
#Percentages of women by top 10 and bottom 10 majors
recent_grads[:10].plot.bar(x='Major', y='ShareWomen', legend=False)
recent_grads[163:].plot.bar(x='Major', y='ShareWomen', legend=False)
# In[38]:
#unemployment rate for top 10 and bottom 10 majors
recent_grads[:10].plot.bar(x='Major', y='Unemployment_rate', legend=False)
recent_grads[163:].plot.bar(x='Major', y='Unemployment_rate', legend=False)
# In[39]:
recent_grads.columns