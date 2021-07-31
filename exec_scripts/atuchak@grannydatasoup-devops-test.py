#!/usr/bin/env python
# coding: utf-8
# In[10]:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv('data/train.csv')['Age'].dropna()
plt.hist(data, bins=int(data.max()-data.min()))
plt.xlabel('Age')
plt.ylabel('N of passengers')
plt.show()
# In[4]:
import random
def partition(a, l, h):
    pivotvalue = a[l]
    leftmark = l + 1
    rightmark = h
    done = False
    while not done:
        while leftmark <= rightmark and a[leftmark] <= pivotvalue:
            leftmark += 1
        while a[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark -= 1
        if rightmark < leftmark:
            done = True
        else:
            a[leftmark], a[rightmark] = a[rightmark], a[leftmark]
    a[l], a[rightmark] = a[rightmark], a[l]
    return rightmark
def qs_(a, l, h):
    if l < h:
        splitpoint = partition(a, l, h)
        qs_(a, l, splitpoint - 1)
        qs_(a, splitpoint + 1, h)
def qs(a):
    qs_(a, 0, len(a)-1)
    
l = random.sample(range(100), 20)
print(l)
qs(l)
print(l)