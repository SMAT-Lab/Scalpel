#!/usr/bin/env python
# coding: utf-8
# In[36]:
import datetime  # for getting current time and timedelta
import time  # for converting to unixtime, for some reason (maybe there is a better way?)
# In[37]:
def convert_datetime_to_unixtime(datetime):
    """convert datetime.datetime to unix time int"""
    return time.mktime(datetime.timetuple())
# In[38]:
def calculate_percentage(total, remaining):
    one_unit = total / 100
    prct = remaining / one_unit
    return(prct)