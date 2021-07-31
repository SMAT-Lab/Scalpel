#!/usr/bin/env python
# coding: utf-8
# In[1]:
from mean import mean
# In[5]:
mean([1,2,3])
# In[6]:
def test_ints():
	numbers = [1,2,3,4,5]   # set of test data
	obs = mean(numbers)     # using function
	exp = 3 				# expected value (you know mean of 1->5)
	assertobs == exp        # if function works, true assertion and therefor no return
# In[9]:
def test_ints():
	numbers = [1,2,3,4,5]   # set of test data
	obs = mean(numbers)     # using function
	exp = 3 				# expected value (you know mean of 1->5)
	assert obs == exp        # if function works, true assertion and therefor no return
# In[10]:
test_ints()
# In[11]:
def test_reals():
	numbers = [1.0,2.0,3.0,4.0,5.0]   # set of test data
	obs = mean(numbers)     # using function
	exp = 3.0 				# expected value (you know mean of 1->5)
	assert obs == exp        # if function works, true assertion and therefor no return
# In[13]:
test_reals()
# In[14]:
def test_long():
	big = 10000 
	exp = big/2.0 # expected average
	obs = mean(range(1,big)) # create list of 1 --> 10000
	assert obs == exp 