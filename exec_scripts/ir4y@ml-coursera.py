#!/usr/bin/env python
# coding: utf-8
# In[1]:
import re
from funcy import *
with open("cats.txt") as c:
    res = [compact(re.split(r'[^a-z]', line.lower())) for line in c.readlines()]
words = list({word for line in res for word in line})
# In[2]:
matrix = [[len([w for w in line if w == word]) for word in words] for line in res]
# In[3]:
import numpy as np
from scipy.spatial.distance import cosine
initial = np.array(matrix[0])
{cosine(initial, np.array(line)): (index + 1) for index, line in enumerate(matrix[1:])}                                                               