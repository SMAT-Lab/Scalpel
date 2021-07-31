#!/usr/bin/env python
# coding: utf-8
# In[3]:
neighbors = [{'name': 'Fred', 'avenue': 4, 'street': 8}, {'name': 'Suzie', 'avenue': 1, 'street': 11}, 
             {'name': 'Bob', 'avenue': 5, 'street': 8}, {'name': 'Edgar', 'avenue': 6, 'street': 13},
             {'name': 'Steven', 'avenue': 3, 'street': 6}, {'name': 'Natalie', 'avenue': 5, 'street': 4}]
# In[5]:
fred = neighbors[0]
natalie = neighbors[5]
# In[7]:
import plotly
plotly.offline.init_notebook_mode(connected=True)
trace0 = dict(x=list(map(lambda neighbor: neighbor['avenue'],neighbors)), 
              y=list(map(lambda neighbor: neighbor['street'],neighbors)),
              text=list(map(lambda neighbor: neighbor['name'],neighbors)),
              mode='markers')
plotly.offline.iplot(dict(data=[trace0], layout={'xaxis': {'dtick': 1}, 'yaxis': {'dtick': 1}}))
# In[9]:
def street_distance(first_neighbor, second_neighbor):
    pass
# In[10]:
street_distance(fred, natalie) # 4
# In[120]:
def avenue_distance(first_neighbor, second_neighbor):
    pass
# In[121]:
avenue_distance(fred, natalie) #  1
# In[122]:
def distance_between_neighbors_squared(first_neighbor, second_neighbor):
    pass
# In[123]:
distance_between_neighbors_squared(fred, natalie) # 17
# In[12]:
import math
def distance(first_neighbor, second_neighbor):
    pass
# In[13]:
distance(fred, natalie) # 4.123105625617661
# In[130]:
import math
def distance_with_neighbor(first_neighbor, second_neighbor):
    pass
# In[131]:
distance_with_neighbor(fred, natalie)
# {'avenue': 5, 'distance': 4.123105625617661, 'name': 'Natalie', 'street': 4}
# In[132]:
def distance_all(first_neighbor, neighbors):
    pass
# In[133]:
distance_all(fred, neighbors)
# [{'avenue': 1, 'distance': 4.242640687119285, 'name': 'Suzie', 'street': 11},
#  {'avenue': 5, 'distance': 1.0, 'name': 'Bob', 'street': 8},
#  {'avenue': 6, 'distance': 5.385164807134504, 'name': 'Edgar', 'street': 13},
#  {'avenue': 3, 'distance': 2.23606797749979, 'name': 'Steven', 'street': 6},
#  {'avenue': 5, 'distance': 4.123105625617661, 'name': 'Natalie', 'street': 4}]
# In[14]:
def nearest_neighbors(first_neighbor, neighbors, number = None):
    pass
# In[15]:
nearest_neighbors(fred, neighbors, 2)
# [{'avenue': 5, 'distance': 1.0, 'name': 'Bob', 'street': 8},
#  {'avenue': 3, 'distance': 2.23606797749979, 'name': 'Steven', 'street': 6}]