#!/usr/bin/env python
# coding: utf-8
# In[1]:
def foo():
    return 'foo'
# In[2]:
bar = 'hi'
# In[1]:
WAT = 'boo'
# In[2]:
class RAWR:
    def rawr(self):
       return 'rawr'
# In[3]:
# This will be not picked up by the defs only importer
r = RAWR()
print(r.rawr())