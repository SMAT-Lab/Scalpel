#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
# In[2]:
def activate(x):
    return 1/(1+np.exp(-x))
def activateDx(x):
    return x*(1-x)
# In[3]:
X = np.array([
    [0,0,1],
    [0,1,1],
    [1,0,1],
    [1,1,1]
])
y = np.array([
    [0],
    [1],
    [1],
    [0]
])
# In[4]:
X
# In[5]:
y
# In[6]:
np.random.seed(1)
syn0 = 2*np.random.random((3,4)) - 1 
syn1 = 2*np.random.random((4,1)) - 1
# In[7]:
print('syn0:\n', syn0)
print('syn1:\n', syn1)
# In[8]:
epochs = 10_000
print_every = 1_000
# In[9]:
for j in range(epochs):
    l0 = X
    l1 = activate(np.dot(l0, syn0))
    l2 = activate(np.dot(l1, syn1))
    # what is a difference between what we've got and expected
    l2_error = y - l2
    if (j % print_every) == 0:
        print('Error:', np.mean(np.abs(l2_error)))
    # determine delta to update weights
    l2_delta = l2_error * activateDx(l2)
    # determine how prev layer participated in final error
    l1_error = l2_delta.dot(syn1.T)
    # determine delta to update weights of the first layer
    l1_delta = l1_error * activateDx(l1)
    # update weights
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)
# In[10]:
def test(x):
    y = activate(np.dot(x, syn0))
    y = activate(np.dot(y, syn1))    
    return 1 if y[0] > 0.5 else 0, y[0]
# In[11]:
test(np.array(np.array([0,0,1])))
# In[12]:
test(np.array(np.array([0,1,1])))