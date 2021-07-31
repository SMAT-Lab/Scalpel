#!/usr/bin/env python
# coding: utf-8
# In[1]:
import re
def tokenize(text: str):
    return re.findall('[a-z]+', text.lower())
# In[12]:
from difflib import SequenceMatcher
def print_matches(subject, query):
    
    s_tokens = tokenize(subject)
    q_tokens = tokenize(query)
    
    matcher = SequenceMatcher(a=s_tokens, b=q_tokens, autojunk=False)
    
    for m in matcher.get_matching_blocks():
        print(s_tokens[m.a:m.a+m.size])
# In[16]:
with open('data/pg284.txt') as fh:
    house_of_mirth = fh.read()
    
with open('data/pg2891.txt') as fh:
    howards_end = fh.read()
# In[17]:
print_matches(house_of_mirth, howards_end)