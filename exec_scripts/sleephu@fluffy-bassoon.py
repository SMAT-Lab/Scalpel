#!/usr/bin/env python
# coding: utf-8
# In[9]:
# HW1:
'''
 How can you handle duplicate values in a dataset in Python?
''' 
# a. use numpy.unique
import numpy as np
array = np.array([1, 1, 2, 2, 3, 4])
array = np.unique(array)
array
# In[10]:
# HW1
# b. use control flow
mylist = [2,3,3,4,4,4,5,1]
out = []
for i in mylist:
    if i not in out:
        out.append(i)
out
# In[13]:
# HW1
# c. use Data structre: set, which only store unique elements
mylist = [2,3,3,4,4,4,5,1]
out = set()
for i in mylist:
    out.add(i)
out
# In[2]:
#HW3: write Python scripts to identify the issuer of the credit card numbers
'''
“Issuer” of a credit card are companies like Visa,
Mastercard, American Express. Now we know the
following rules:
CC number starts with: '4'
CC len : 16
Issuer: VISA
CC number starts with: '34', '37'
CC len : 15
Issuer : AMEX
CC number starts with: '36'
CC len : 14
Issuer : Diners Club
Credit card number starts with
'4026', '417500', '4405', '4508', '4844',
'4913', '4917'
CC len : 16
Issuer : VISAELECTRON
'''
def validate(cc):
    if len(cc) == 15 and ((cc[0:2] == "34") or (cc[0:2] == "37")):
        print("AMEX")
    elif (cc[0:2] == "36") and (len(cc) == 14):
        print("Diners Club")
    elif (cc[0:1] == "4") and (len(cc) == 16):
        if (cc[0:6] == "417500"):
            print("VISTAELECTION")
        else:
            print("VISA")
    else:
        print("N/A")
cc = "4175004175004172"
validate(cc)
# In[1]:
# cumulative time series
# In[2]:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# In[3]:
# read data
# file_location = "/..."
# file_name = 'data.csv'
my_data = pd.read_csv('data.csv')
my_data.head(5)
# In[4]:
# deal with data
import datetime
my_data.date = pd.to_datetime(my_data.date, format = '%Y%m%d')
# In[5]:
# function: get cummulative series for each id
def getCumSeries(my_data, my_id, country, vertical):
    # filter certain country, vertical's date and spend_usd
    table = my_data[['date', 'spend_usd']][(my_data.experiment_id == my_id) & (my_data.country == country) & (my_data.vertical == vertical)]
    # calculate sum of spend_usd, group by date 
    data = table.groupby('date')['spend_usd'].sum()
    # calculate cumulative sum for data
    data = np.cumsum(data)
    # get total_revenue (last row)
    total_revenue = data[-1]
    return((data, total_revenue))
# In[6]:
# test
blue = getCumSeries(my_data, 12624549, 'JP', 'ANDROID_APPS')
blue
# In[7]:
import matplotlib.ticker as mtick
def plotSeries(experiment_series, control_series, country, vertical):
    fig, ax = plt.subplots()
    ax.plot(experiment_series, color = "red", label = "experiment")
    ax.plot(control_series, color = "blue", label = "control")
    # tweaks
    ax.set_ylim(0, 100000)
    ax.set_title(country + " " + vertical + " " + "experiment v.s control")
    ax.set_ylabel("Total Spend")
    ax.grid(True, which = "both")
    fmt = '${x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick) 
    # change legend
    ax.legend().get_texts()[0].set_text("experiment")
    ax.legend().get_texts()[1].set_text("control")
    # format date
    plt.gcf().autofmt_xdate()
# In[8]:
def printCumSeries(my_data, experiment_ids, country, vertical):
    # get unique date
    index_series = np.unique(my_data.date)
    # sort date
    index_series = np.sort(index_series)
    # group by date
    my_data = my_data.sort_values("date", ascending = True, inplace = False)
    # get cumulative series and total revenue respectively
    treatment_series = getCumSeries(my_data, experiment_ids[0], country, vertical)[0]
    treatment_revenue = getCumSeries(my_data, experiment_ids[0], country, vertical)[1]
    control_series = getCumSeries(my_data, experiment_ids[1], country, vertical)[0]
    control_revenue = getCumSeries(my_data, experiment_ids[1], country, vertical)[1]
    
    # print out overall uplift
    print("Overall % uplift on revenue:" + str((treatment_revenue - control_revenue)/control_revenue))
    # plot
    plotSeries(treatment_series, control_series, country, vertical)
# In[9]:
printCumSeries(my_data, [12624548, 12624549], 'JP', 'ANDROID_APPS')
# In[10]:
printCumSeries(my_data, [12624548,12624549], 'US', 'ANDROID_APPS')