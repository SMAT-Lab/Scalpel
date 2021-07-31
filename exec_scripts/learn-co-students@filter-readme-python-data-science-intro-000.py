#!/usr/bin/env python
# coding: utf-8
# In[11]:
7 % 3
# In[1]:
6 % 3
# In[30]:
4 % 2
# In[8]:
def is_even(number):
    return number % 2 == 0
# In[9]:
print(is_even(3)) # False
print(is_even(100)) # True
# In[10]:
def select_even(elements):
    selected = []
    for element in elements:
        if is_even(element):
            selected.append(element)
    return selected
# In[11]:
numbers = list(range(0, 11))
numbers
# In[12]:
select_even(numbers)
# In[4]:
def ends_ing(word):
    return word.endswith('ing')
def select_ing(elements):
    selected = []
    for element in elements:
        if ends_ing(element):
            selected.append(element)
    return selected
words = ['camping', 'biking', 'sailed', 'swam']
select_ing(words)
# In[13]:
filter(is_even,numbers)
# In[9]:
list(filter(is_even, numbers))
# In[54]:
list(filter(ends_ing, words))
# In[18]:
random_list = [0,'0','python', 2, True, 'flatiron', False, 38.9]
# In[19]:
list(filter(None, random_list))