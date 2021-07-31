#!/usr/bin/env python
# coding: utf-8
# In[2]:
abs(-3)
# In[6]:
all([True, True, True])
# In[7]:
all([True, True, False])
# In[8]:
all([])
# In[10]:
any([True, True, False])
# In[11]:
any([False, False, False])
# In[12]:
any([])
# In[17]:
bin(42)
# In[24]:
bool(True)
# In[25]:
bool([True])
# In[29]:
bool(False)
# In[30]:
bool([False])
# In[31]:
bool([])
# In[66]:
bytearray(4)
# In[64]:
bytes(4)
# In[53]:
callable(7)
# In[55]:
callable(int)
# In[49]:
chr(97)
# In[50]:
chr(8364)
# In[88]:
class Bar:
    @classmethod
    def foo(cls, arg1):
        print(arg1)
# In[89]:
Bar
# In[90]:
Bar.foo
# In[91]:
Bar.foo('hello')
# In[93]:
Bar()
# In[97]:
Bar().foo('hello')