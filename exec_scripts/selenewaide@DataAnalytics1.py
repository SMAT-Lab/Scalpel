#!/usr/bin/env python
# coding: utf-8
# In[147]:
# Import pandas, numpy and matplotlib libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns # used for plots and pairwise feature interactions
from matplotlib.backends.backend_pdf import PdfPages
get_ipython().run_line_magic('matplotlib', 'inline')
# In[148]:
# Reading from a csv file, into a data frame
# This csv file is in the same folder and the notebook file, therefore it does not need a full path
df = pd.read_csv('amazon-offers-10k-samples-raw.csv')
# In[149]:
# Number of rows and columns in this dataframe displayed as (row no., column no.)
df.shape
# In[150]:
df.head(5) # first 5 rows
# In[151]:
df.tail(5) # last 5 rows
# In[152]:
# Show the data types in each column
# The pandas type 'object' stands for Python strings
# Columns mixing numbers and characters are automatically converted to type 'object'
df.dtypes
# In[153]:
# Select columns containing categorical data
categorical_columns = df[['IsWinner','IsFeaturedMerchant','IsFulfilledByAmazon','ListingCurrency','ShippingCurrency', 'ShippingTime_availtype', 'ShipsDomestically', 'ShipsFromCountry', 'ShipsFromState', 'SubCondition']].columns
# Convert data type to category for these columns
for column in categorical_columns:
    df[column] = df[column].astype('category')
# In[154]:
# data types after the conversion
df.dtypes
# In[155]:
# Descriptive stats for continuous features
df.describe()
# In[156]:
# Descriptive stats for continuous features - transposed table
# One feature per row, stats in the columns
df.describe().T
# In[157]:
# Descriptive stats for categorical features
df.select_dtypes(['category']).describe().T
# In[158]:
# duplicated(): returns a boolean - outputs 'true' is an entire row is a duplicate of a row above it.
# The 'true' instances are then counted using sum()
df.duplicated().sum()
# In[159]:
# using drop_duplicates(), default is keep ='first' as parameter.
df = df.drop_duplicates()
# In[160]:
df.duplicated().sum() # check again for duplicates
# In[161]:
# After duplicated rows removed
df.shape
# In[162]:
# Print all the coloumn headers and the number of unique values in each coloumn
# Coloumns with unique value of 1 has a constant value 
print("Feature, UniqueValues") 
for column in df:
    print(column + "," + str(len(df[column].unique())))
# In[163]:
# Drop columns with UniqueValues = 1
# Feature, UniqueValues
# MarketplaceId,1
# ListingCurrency,1
# ShippingCurrency,1
# ShippingTime_availtype,1
# ShipsDomestically,1
# SubCondition,1
# The '1' below indicates column:
df = df.drop('MarketplaceId', 1)
df = df.drop('ListingCurrency', 1)
df = df.drop('ShippingCurrency', 1)
df = df.drop('ShippingTime_availtype', 1)
df = df.drop('ShipsDomestically', 1)
df = df.drop('SubCondition', 1)
# In[164]:
df.shape # after 6 columns of constant columns removed
# In[165]:
#Look at continous columns - all of which are of numeric data type in this data frame
continuous_columns = df.select_dtypes(['int64', 'float64']).columns
continuous_columns
# In[166]:
# Descriptive stats for continuous features - transposed table
df[continuous_columns].describe().T
# In[167]:
#Look at categorical columns - marked as 'category' data type
categorical_columns = df.select_dtypes(['category']).columns
categorical_columns
# In[168]:
# Descriptive stats for categorical features
df[categorical_columns].describe().T
# In[169]:
# Plot a histogram of the continuous features
df[continuous_columns].hist(figsize=(15,15))
# In[170]:
for col in continuous_columns:
    f = df[col].plot(kind='box', figsize=(5,5))
    plt.show()
# In[171]:
for column in categorical_columns:
    f = df[column].value_counts().plot(kind='bar', title=column, figsize=(8,5))
    plt.show()
# In[172]:
# Check for irregular cardinality in categorical features. There could be same values spelled differently
print("Unique values for:\n- IsWinner:", pd.unique(df.IsWinner.ravel()))
print("\n- IsFeaturedMerchant:", pd.unique(df.IsFeaturedMerchant.ravel()))
print("\n- IsFulfilledByAmazon:", pd.unique(df.IsFulfilledByAmazon.ravel()))
print("\n- ShipsFromCountry:", pd.unique(df.ShipsFromCountry.ravel()))
print("\n- ShipsFromState:", pd.unique(df.ShipsFromState.ravel()))
# In[173]:
# Check whether there are null values in the data where values would be expected
df.isnull().sum()
# In[174]:
# Find out the 5 highest ListingPrices
df.sort_values(by='ListingPrice', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last').head(5)
# In[175]:
df_O1 = df.loc[df['ProductId'] == 2471683711038624825]
df_O1.head(5)
# In[176]:
df_O1['ListingPrice'].plot(kind='hist')
# In[177]:
df_O2 = df.loc[df['ProductId'] == 1711327863243739776]
df_O2.head(5)
# In[178]:
df_O2['ListingPrice'].plot(kind='hist')
# In[179]:
df_O3 = df.loc[df['ProductId'] == -5924928993300787167]
df_O3.head(5)
# In[180]:
df_O3['ListingPrice'].plot(kind='hist')
# In[181]:
# Find out the 5 highest ShipppingPrice
df.sort_values(by='ShippingPrice', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last').head(5)
# In[182]:
df_O4 = df.loc[df['SellerId'] == -6639690782514669126]
df_O4.head(5)
# In[183]:
df_O4['ShippingPrice'].plot(kind='hist')
# In[184]:
# Find out the 5 highest SellerFeedbackRating
df.sort_values(by='SellerFeedbackRating', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last').head(5)
# In[185]:
# Find out the 5 highest SellerFeedbackCount
df.sort_values(by='SellerFeedbackCount', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last').head(5)
# In[186]:
# Find out the 5 highest ShippingTime_minHours
df.sort_values(by='ShippingTime_minHours', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last').head(5)
# In[187]:
# Find out the 5 highest ShippingTime_maxHours
df.sort_values(by='ShippingTime_maxHours', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last').head(5)
# In[188]:
# generating another dataframe called df_cleaned and applying changes to it
# Dropping ListingPrice outliers:
clean_df = df
clean_df = clean_df.drop(clean_df.index[[9069,9069]])
clean_df = clean_df.drop(clean_df.index[[6890,6890]])
clean_df = clean_df.drop(clean_df.index[[4947,4947]])
clean_df = clean_df.drop(clean_df.index[[152,152]])
clean_df = clean_df.drop(clean_df.index[[4830,4830]])
# In[189]:
# Dropping ShippingPrice outliers:
clean_df = clean_df.drop(clean_df.index[[1343,1343]])
clean_df = clean_df.drop(clean_df.index[[7392,7392]])
clean_df = clean_df.drop(clean_df.index[[5775,5775]])
clean_df = clean_df.drop(clean_df.index[[610,610]])
clean_df = clean_df.drop(clean_df.index[[5067,5067]])
# In[190]:
# shape of new dataframe after outliers dropped per cells above.
clean_df.shape
# In[191]:
# shape of original dataframe - no outliers dropped
df.shape
# In[192]:
# Save cleaned dataframe to new CSV file
clean_df.to_csv('amazon-offers-samples-raw-cleaned.csv', index=False)
clean_df.head(5)
# In[193]:
# Counts the number of IsFeaturedMerchant = 0 (i.e. negative result)
NotFeaturedMerchant_count = 1 / clean_df[clean_df.IsFeaturedMerchant == 0].count()['IsFeaturedMerchant']
# Counts the number of IsFeaturedMerchant = 1 (i.e. positive result)
IsFeaturedMerchant_count = 1 / clean_df[clean_df.IsFeaturedMerchant == 1].count()['IsFeaturedMerchant']
# Create a new column in the dataframe called percent and insert IsFeaturedMerchant_count in all cells
clean_df['percent'] = IsFeaturedMerchant_count * 100
# Find indexes of all rows containing negative value for IsFeaturedMerchant
index_list = clean_df[clean_df['IsFeaturedMerchant'] == 0].index.tolist()
# For each row with a 0 value, insert NotFeaturedMerchant_count in the percent column
for i in index_list:
    clean_df.loc[i, 'percent'] = NotFeaturedMerchant_count * 100
# Group dataframe by IsFeaturedMerchant and IsWinner and sum precent
category_group = clean_df[['percent','IsFeaturedMerchant','IsWinner']].groupby(['IsFeaturedMerchant','IsWinner']).sum()
# Plot values of category_group in a stacked bar chart
my_plot = category_group.unstack().plot(kind='bar', stacked=True, title="IsWinner by IsFeaturedMerchant", figsize=(13,7))
# Define legend colours and text and add to the plot
red_patch = mpatches.Patch(color='green', label='IsWinner')
blue_patch = mpatches.Patch(color='blue', label='NotWinner')
my_plot.legend(handles=[red_patch, blue_patch], frameon = True)
# Define x and y labels and min and max values for the y axis
my_plot.set_xlabel("IsFeaturedMerchant")
my_plot.set_ylabel("% IsWinner")
my_plot.set_ylim([0,100])
# In[194]:
# Counts the number of IsFulfilledByAmazon = 0 (i.e. negative result)
NotFulfilledByAmazon_count = 1 / clean_df[clean_df.IsFulfilledByAmazon == 0].count()['IsFulfilledByAmazon']
# Counts the number of IsFulfilledByAmazon = 1 (i.e. positive result)
IsFulfilledByAmazon_count = 1 / clean_df[clean_df.IsFulfilledByAmazon == 1].count()['IsFulfilledByAmazon']
# Create a new column in the dataframe called percent and insert IsFulfilledByAmazon_count in all cells
clean_df['percent'] = IsFulfilledByAmazon_count * 100
# Find indexes of all rows containing negative value for IsFulfilledByAmazon
index_list = clean_df[clean_df['IsFulfilledByAmazon'] == 0].index.tolist()
# For each row with a 0 value, insert NotFulfilledByAmazon_count in the percent column
for i in index_list:
    clean_df.loc[i, 'percent'] = NotFulfilledByAmazon_count * 100
# Group dataframe by IsFulfilledByAmazon and IsWinner and sum precent
category_group = clean_df[['percent','IsFulfilledByAmazon','IsWinner']].groupby(['IsFulfilledByAmazon','IsWinner']).sum()
# Plot values of category_group in a stacked bar chart
my_plot = category_group.unstack().plot(kind='bar', stacked=True, title="IsWinner by IsFulfilledByAmazon", figsize=(13,7))
# Define legend colours and text and add to the plot
red_patch = mpatches.Patch(color='green', label='IsWinner')
blue_patch = mpatches.Patch(color='blue', label='NotWinner')
my_plot.legend(handles=[red_patch, blue_patch], frameon = True)
# Define x and y labels and min and max values for the y axis
my_plot.set_xlabel("IsFulfilledByAmazon")
my_plot.set_ylabel("% IsWinner")
my_plot.set_ylim([0,100])
# In[195]:
# List unique values in ShipsFromCountry
shipsfromcountries = pd.unique(clean_df.ShipsFromCountry.ravel())
# Insert new column in df called 'percent' and fill with 0s
clean_df['percent'] = 0
# Iterate through the unique values in ShipsFromCountry and for each value count the amount of IsWinner 
# Find the indexes of each row in a particular ShipsFromCountry and for each of these row insert count * 100 in the percent column
for c in shipsfromcountries:
    count = 1 / clean_df[clean_df.ShipsFromCountry == c].count()['IsWinner']
    index_list = clean_df[clean_df['ShipsFromCountry'] == c].index.tolist()
    for i in index_list:
        clean_df.loc[i, 'percent'] = count * 100
        
# Group dataframe by ShipsFromCountry and IsWinner and sum
group = clean_df[['percent','ShipsFromCountry','IsWinner']].groupby(['ShipsFromCountry','IsWinner']).sum()
# Plot values of group in a stacked bar chart
my_plot = group.unstack().plot(kind='bar', stacked=True, title="IsWinner by ShipsFromCountry", figsize=(15,7))
# Define label colours and text and add to the plot
red_patch = mpatches.Patch(color='green', label='IsWinner')
blue_patch = mpatches.Patch(color='blue', label='Not IsWinner')
my_plot.legend(handles=[red_patch, blue_patch], frameon = True)
# Define x and y labels and min and max values for the y axis
my_plot.set_xlabel("ShipsFromCountry")
my_plot.set_ylabel("% IsWinner")
my_plot.set_ylim([0,100])
# In[196]:
# List unique values in ShipsFromState
shipsfromstates = pd.unique(clean_df.ShipsFromState.ravel())
# Insert new column in df called 'percent' and fill with 0s
clean_df['percent'] = 0
# Iterate through the unique values in ShipsFromState and for each value count the amount of IsWinner 
# Find the indexes of each row in a particular ShipsFromState and for each of these row insert count * 100 in the percent column
for c in shipsfromstates:
    count = 1 / clean_df[clean_df.ShipsFromState == c].count()['IsWinner']
    index_list = clean_df[clean_df['ShipsFromState'] == c].index.tolist()
    for i in index_list:
        clean_df.loc[i, 'percent'] = count * 100
        
# Group dataframe by ShipsFromState and IsWinner and sum
group = clean_df[['percent','ShipsFromState','IsWinner']].groupby(['ShipsFromState','IsWinner']).sum()
# Plot values of group in a stacked bar chart
my_plot = group.unstack().plot(kind='bar', stacked=True, title="IsWinner Candidate by ShipsFromState", figsize=(15,7))
# Define label colours and text and add to the plot
red_patch = mpatches.Patch(color='green', label='IsWinner')
blue_patch = mpatches.Patch(color='blue', label='Not IsWinner')
my_plot.legend(handles=[red_patch, blue_patch], frameon = True)
# Define x and y labels and min and max values for the y axis
my_plot.set_xlabel("ShipsFromState")
my_plot.set_ylabel("% IsWinner")
my_plot.set_ylim([0,100])
# In[197]:
plt.figure()
flierprops = dict(marker='o', markerfacecolor='green', markersize=6,
                  linestyle='none')
bp = clean_df.boxplot(column=['ListingPrice'], by=['IsWinner'], flierprops=flierprops, figsize=(10,7))
bp = clean_df.boxplot(column=['SellerFeedbackRating'], by=['IsWinner'], flierprops=flierprops, figsize=(10,7))
bp = clean_df.boxplot(column=['SellerFeedbackCount'], by=['IsWinner'], flierprops=flierprops, figsize=(10,7))
# In[198]:
# Correlation matrix using code found on https://stanford.edu/~mwaskom/software/seaborn/examples/many_pairwise_correlations.html
clean_df = pd.read_csv('amazon-offers-samples-raw-cleaned.csv')
sns.set(style="white")
# Select columns containing continuous data
continuous_columns = clean_df[['ListingPrice','SellerFeedbackRating','SellerFeedbackCount','ShippingPrice']].columns
# Calculate correlation of all pairs of continuous features
corr = clean_df[continuous_columns].corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))
# Generate a custom colormap - blue and red
cmap = sns.diverging_palette(220, 10, as_cmap=True)
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, annot=True, mask=mask, cmap=cmap, vmax=1, vmin=-1,
            square=True, xticklabels=True, yticklabels=True,
            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
plt.yticks(rotation = 0)
plt.xticks(rotation = 45)