#!/usr/bin/env python
# coding: utf-8
# In[15]:
from datetime import datetime, timedelta
start_date = datetime(2018, 1, 30)
print('Start Date of Long Service Leave is', start_date.strftime('%a %Y-%m-%d'))
paid_weeks = 347.32//7.6/5 * 2
end_date = start_date + timedelta(weeks=paid_weeks)
print('Paid Weeks:', paid_weeks)
print('Start Date of Long Service Leave is', end_date.strftime('%a %Y-%m-%d'))