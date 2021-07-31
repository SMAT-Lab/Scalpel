#!/usr/bin/env python
# coding: utf-8
# In[3]:
import datetime
# current date and time object
now = datetime.datetime.now()
print(now.year)
print(now.hour)
print(now.minute)
# Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
print(now.weekday())
# In[6]:
dt_obj = datetime.datetime(2018, 11, 10, 17, 53, 59)
date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
date_str
# In[8]:
date_str = "2008-11-10 17:53:59"
dt_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
dt_obj
# In[10]:
# timestamp to datetime object in UTC
timestamp = 1226527167.595983
dt_obj = datetime.datetime.utcfromtimestamp(timestamp)
dt_obj
# In[11]:
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=8)
difference_in_days = abs((end_date - start_date).days)
# In[12]:
difference_in_days