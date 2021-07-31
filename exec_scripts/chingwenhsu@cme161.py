#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from random import randrange
import datetime 
import random
import json
n = 1000
# In[2]:
weight = np.random.randn(n) + 50
plt.hist(weight, bins = 10)
plt.xlim(45,55)
# In[3]:
sleep_hour = 0.3*np.random.randn(n)+7.5
plt.hist(sleep_hour, bins= 10)
plt.xlim(5,10)
# In[4]:
sport_hour = abs(0.5*np.random.randn(n)+0.2)
plt.hist(sport_hour)
plt.xlim(0,2)
# In[5]:
work_hour = 1*np.random.randn(n)+7.5
plt.hist(work_hour)
plt.xlim(4,12)
# In[6]:
basal_temp = 0.1*np.random.randn(n)+36.45
plt.hist(basal_temp, bins=10)
plt.xlim([36, 36.9])
# In[7]:
def random_date(start,l):
   current = start
   while l >= 0:
      curr = current + datetime.timedelta(minutes=randrange(120))
      yield curr
      l-=1
startDate = datetime.datetime(2016,5,5,7,00)
wakeup_time = []
for x in random_date(startDate,n):
    wakeup_time.append(x.strftime("%H:%M"))
print(wakeup_time) 
startDate = datetime.datetime(2016,5,5,22,00)
sleep_time = []
for x in random_date(startDate,n):
    sleep_time.append(x.strftime("%H:%M"))
print(sleep_time) 
# In[15]:
dt = datetime.datetime(2010, 1, 1)
step = datetime.timedelta(days=1)
i = 1
date = []
while True:
    date.append(dt.strftime('%Y-%m-%d'))
    dt += step
    i += 1
    if i > n:
        break
    
date
# In[9]:
room_temp = 3*np.random.randn(n)+25
plt.hist(room_temp, bins=10)
plt.xlim([15, 35])
# In[10]:
# condition = np.random.binomial(1, 0.3, n)
condition = []
for _ in range(n):
    x = np.random.randn(1)
    if x < -1:
        condition.append("bad")
    elif x > 0.5:
        condition.append("excellent")
    else:
        condition.append("so-so")
condition
# In[11]:
weather = []
for _ in range (n):
    x = np.random.randn(1)
    if x < -0.5:
        weather.append("cloudy")
    elif x > 0.9:
        weather.append("rainy")
    else:
        weather.append("sunny")
    
weather
# In[12]:
mood = []
for _ in range(n):
    x = np.random.randn(1)
    if x > 0.5:
        mood.append(":D")
    elif x < -1:
        mood.append(":(")
    else:
        mood.append(":)")
mood
# In[16]:
def generate_data(date, wakeup, sleep, condition, room_temp, basal_temp, weight, sleep_hour, mood, 
                  weather, work_hour, sport_hour):
    return {"date": date,
            "wakeup_time": wakeup,
            "sleep_time": sleep,
            "condition" : condition,
            "room_temp": room_temp,
            "basal_temp" : basal_temp,
            "weight" : weight,
            "sleep_hour" : sleep_hour,
            "mood" : mood,
            "weather": weather,
            "work_hour": work_hour,
            "sport_hour": sport_hour
           }
data = []
for i in range(n):
    data.append(
        generate_data(date[i], wakeup_time[i], sleep_time[i], condition[i], room_temp[i], basal_temp[i], 
                      weight[i], sleep_hour[i], mood[i], weather[i],work_hour[i], sport_hour[i])
    )
# In[14]:
len(date)