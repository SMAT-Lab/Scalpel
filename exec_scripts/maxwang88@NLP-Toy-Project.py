#!/usr/bin/env python
# coding: utf-8
# In[1]:
import os
# Read in a plain text file
with open(os.path.join("data", "hieroglyph.txt"), "r") as f:
    text = f.read()
    print(text)
# In[8]:
from collections import Counter
words = ['humpy', 'dumpty', 'together', 'again']
counts = Counter(words)
counts['again']