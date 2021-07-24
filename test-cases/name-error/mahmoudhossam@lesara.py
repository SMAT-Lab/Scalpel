#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
# In[2]:
import dill
# In[3]:
import numpy
# In[4]:
get_ipython().run_line_magic('matplotlib', 'inline')
# In[69]:
df = pd.read_csv("orders.csv", parse_dates=["created_at_date"])
# In[6]:
df.head()
# In[8]:
df.keys()
# In[9]:
max_revenue = df[['customer_id', 'revenue']].groupby('customer_id', as_index=True).max()['revenue']
# In[26]:
df[['customer_id', 'order_id']].groupby(['customer_id']).order_id.nunique().to_frame()
# In[11]:
max_items = df[['customer_id', 'num_items']].groupby('customer_id', as_index=True).max()['num_items']
# In[12]:
total_revenue = df[['customer_id', 'revenue']].groupby('customer_id', as_index=True).sum()['revenue']
# In[13]:
days_since_last_order = pd.Timestamp.strptime('2017-10-17', '%Y-%m-%d') - df[['customer_id', 'created_at_date']].groupby('customer_id', as_index=True).max()['created_at_date']
# In[15]:
result = pd.DataFrame({'Max revenue': max_revenue, 'Order count': order_count, 'Max items': max_items, 'Total revenue': total_revenue, 'Days since last order': days_since_last_order})
# In[16]:
model = dill.load(open("model.dill", 'rb'))
# In[17]:
array = numpy.array([[2, 5, 6, 7, 9, 10], [3, 6, 7, 8, 11, 12]])
# In[18]:
model.predict(array)
# In[19]:
df['revenue'].plot()
# In[20]:
result
# In[38]:
customers_orders = df.groupby(['customer_id', 'order_id'])
# In[37]:
def max_items():
    return df.groupby(['customer_id', 'order_id'])['customer_id', 'order_id', 'num_items'].sum().groupby(['customer_id']).max()
# In[29]:
df.head()
# In[71]:
lol = df[['customer_id', 'created_at_date']].groupby('customer_id').max()['created_at_date'].subtract(pd.Timestamp(datetime(2017, 10, 17))).abs().to_frame()
# In[72]:
lol.dtypes