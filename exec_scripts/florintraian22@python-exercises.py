#!/usr/bin/env python
# coding: utf-8
# In[3]:
# Q: What will be the output of the following code and why?
# A: You shouldn't use mutable types as default values when defining a function. 
# The default list gets created when the function gets defined.
# To correct this you should set de default value of list to None and create the list inside the function.
# def extend_list(val, list=None):
#    if list is None:
#        list = []
#    list.append(val)
#    return list
def extend_list(val, list=[]):
    list.append(val)
    return list
list1 = extend_list(10)
list2 = extend_list(123, [])
list3 = extend_list('a')
print('list1 = %s' %list1)
print('list2 = %s' %list2)
print('list3 = %s' %list3)
# In[5]:
# Q: Does the following code produce the output:
# Matrix : [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
# A: No, because the iterator provides the next value until it finishes. 
# In the list comprehension the left part gets evaluated first.
# One solution is to change the iterator into a list
iterator = (i for i in range(1, 4))
matrix = [[x*y for y in iterator] for x in iterator]
print ("Matrix: %s" %str(matrix))
# In[12]:
# Q: How are variables passed in python, through by reference or by value?
# A: Always by reference.
# Possible gotchas:
def add_ten(a):
    a+=10
    
x = 20
add_ten(x)
print('x = %s' %x)
# x remains 20 because integers are immutable.
# Helper example would be:
def append_ten(list):
    list.append(10)
    
list1 = []
append_ten(list1)
append_ten(list1)
append_ten(list1)
print('list1: %s' %str(list1))
# Lists are mutable.
# In[16]:
# Q: What will the following code output?
# This is an advanced question, not really used lately.
# You can fix this by giving the lambda function a default argument like so:
# function_list = [lambda x, i=i: x*i for i in range(5)]
function_list = [lambda x: x*i for i in range(5)]
for func in function_list:
    print(func(2))