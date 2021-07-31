#!/usr/bin/env python
# coding: utf-8
# In[8]:
class Node(object):
    def __init__(self, value):
        self.value = value # setup a value
        self.nextnode = None # stup a nextnode
# In[2]:
a = Node(1)
b = Node(2)
c = Node(3)
# In[3]:
a.nextnode = b
b.nextnode = c
# In[4]:
a.value
# In[7]:
a.nextnode.nextnode.value