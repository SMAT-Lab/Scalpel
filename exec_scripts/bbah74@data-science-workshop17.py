#!/usr/bin/env python
# coding: utf-8
# In[69]:
# Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette('Dark2')
plt.rcParams['figure.figsize'] = (8,6)
get_ipython().run_line_magic('matplotlib', 'inline')
# In[29]:
# Importing the dataset using the pandas function ``read_csv``
iris = pd.read_csv('iris.csv')
type(iris)
# In[30]:
# Display some information
iris.info()
# In[31]:
iris.head(5)
# In[32]:
iris.tail(5)
# In[33]:
# If I want to know the how many unique species I have in my DataFrame :
iris.Species.value_counts()
# In[34]:
iris.Sepal_Width
# Note that if your column name includes spaces, commas or dots the previous line won't work
# In this case use instead (uncomment the line to check) :
#iris['Sepal_Width']
# In[35]:
setosa = iris.query("Species == 'setosa'")
# Equivalently you can use :
#setosa = iris[iris.Species == 'setosa']
setosa.head(5)
# In[36]:
versicolor = iris.query("Species == 'versicolor'")
virginica = iris.query("Species == 'virginica'")
# In[37]:
iris.query("Sepal_Length > 6.5 and Sepal_Width < 3.0")
# In[38]:
# accessing a column :
#iris.iloc[:,0]
# accessing a row
iris.iloc[0,:]
# In[39]:
# accessing a position directly
iris.iloc[2,2]
# In[40]:
# Try the following like this and then without the .copy() and notice the difference
# ps: you might need to reload the data if you haven't noticed anything...
sepal_width = setosa.Sepal_Width.copy()
sepal_width.replace(3.0, 0.0, inplace=True)
setosa.Sepal_Width
# In[41]:
# Let's just reload the iris dataset... just in case
iris = pd.read_csv('iris.csv')
# In[42]:
iris.Sepal_Length.plot.hist()
# In[43]:
# Alternatively we can include the kde estimation using seaborn library
# First let's make a figure with two subplots
fig, ax = plt.subplots(nrows=1, ncols=2)
sns.distplot(iris.Sepal_Length, ax=ax[0])
sns.kdeplot(iris.Sepal_Length, ax=ax[1])
# In[44]:
iris.plot.scatter(x='Sepal_Length', y='Sepal_Width', s=30)
# In[47]:
species_cols = iris.Species.replace({'setosa':'C0','versicolor':'C1','virginica':'C2'})
# In[48]:
iris.plot.scatter(x='Sepal_Length', y='Sepal_Width', c=species_cols, s=30)
# In[49]:
iris.plot.scatter(x='Petal_Length', y='Petal_Width', c=species_cols, s=30)
# In[50]:
sns.pairplot(data=iris, hue='Species')
# In[51]:
# Using built-in pandas hexbin
iris.plot.hexbin(x='Sepal_Length', y='Sepal_Width', cmap='Blues', gridsize=21, mincnt=1)
# In[52]:
# Using a kde extrapolation
sns.kdeplot(iris['Sepal_Width'], iris['Sepal_Length'],
            cmap="Blues", shade=False, shade_lowest=False)
# In[53]:
# Subset the iris dataset by species
setosa = iris.query("Species == 'setosa'")
versicolor = iris.query("Species == 'versicolor'")
virginica = iris.query("Species == 'virginica'")
# Draw the two density plots
ax = sns.kdeplot(setosa['Sepal_Width'], setosa['Sepal_Length'],
                 cmap="Greens", shade=False, shade_lowest=False)
sns.kdeplot(versicolor['Sepal_Width'], versicolor['Sepal_Length'],
            cmap="Oranges", shade=False, shade_lowest=False, ax=ax)
sns.kdeplot(virginica['Sepal_Width'], virginica['Sepal_Length'],
            cmap="Purples", shade=False, shade_lowest=False, ax=ax)
# In[54]:
g = sns.PairGrid(iris, diag_sharey=False)
g.map_lower(sns.kdeplot)
g.map_upper(plt.scatter)
g.map_diag(sns.distplot)
# In[55]:
iris.describe()
# In[56]:
iris.boxplot()
# In[57]:
groups = iris.groupby(by='Species', as_index=True)
# If you then need to extract the setosa for instance then use the command
#groups.get_group('setosa')
# In[58]:
groups.describe()
# In[59]:
# additionl information can be retrieved using more specific functions
groups.skew()
# In[60]:
_ = groups.boxplot(figsize=(14,10))
# In[61]:
iris_corr = iris.corr()
sns.heatmap(iris_corr, annot=True, fmt='0.2f', cmap='Greens')
# In[62]:
setosa = groups.get_group('setosa')
versicolor = groups.get_group('versicolor')
virginica = groups.get_group('virginica')
plt.figure(figsize=(14,12))
ax1 = plt.subplot(221)
sns.heatmap(setosa.corr(), annot=True, fmt='0.2f', cmap='Greens', ax=ax1)
ax1.set_title('setosa', fontsize=15)
ax2 = plt.subplot(223)
sns.heatmap(versicolor.corr(), annot=True, fmt='0.2f', cmap='Oranges', ax=ax2)
ax2.set_title('versicolor', fontsize=15)
ax3 = plt.subplot(224)
sns.heatmap(virginica.corr(), annot=True, fmt='0.2f', cmap='Purples', ax=ax3)
ax3.set_title('virginica', fontsize=15)