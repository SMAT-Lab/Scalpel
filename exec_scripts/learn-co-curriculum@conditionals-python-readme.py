#!/usr/bin/env python
# coding: utf-8
# In[2]:
vacation_days = 0
vacation_days += 1
vacation_days += 1
vacation_days
# In[3]:
vacation_days = 1
if False:
    # code does not run as conditional argument False
    vacation_days += 1
# In[4]:
vacation_days
# In[5]:
vacation_days = 1
if False:
    # if block begins
    vacation_days += 1
# if block ends
vacation_days += 2
vacation_days
# In[6]:
vacation_days = 1
if True:
    # code in if block runs, as True
    vacation_days += 1
vacation_days
# In[7]:
def long_vacation(number_of_days):
    if number_of_days > 4:
        return 'that is a long vacation'
# In[8]:
long_vacation(5) # 'that is a long vacation'
# In[9]:
long_vacation(3) # None
# In[10]:
def vacation_length(number_of_days):
    if number_of_days > 4:
        return 'that is a long vacation'
    else:
        return 'not so long'
# In[11]:
vacation_length(3) # 'not so long'
# In[12]:
vacation_length(5) # 'that is a long vacation'
# In[13]:
vacation_days = 1
if vacation_days:
    # this is run
    vacation_days += 1
vacation_days
# In[14]:
vacation_days = 0
if vacation_days:
    # this is not run
    vacation_days += 1
vacation_days
# In[15]:
greeting = ''
if greeting:
    greeting += 'Hello'
else:
    greeting += 'Goodbye'
greeting
# In[16]:
bool(0) # False
# In[17]:
bool(1) # True
# In[18]:
greetings = ['hello', 'bonjour', 'hola', 'hallo', 'ciao', 'ola', 'namaste', 'salam']
def starts_with_h(words):
    selected = []
    for word in words:
        if word.startswith('h'):
            selected.append(word)
    return selected 
starts_with_h(greetings)