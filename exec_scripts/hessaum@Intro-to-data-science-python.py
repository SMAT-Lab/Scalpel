#!/usr/bin/env python
# coding: utf-8
# In[2]:
x = 1
y = 2
x + y
# In[1]:
# Sample addition of two numbers
def add_numbers(x, y):
    return x + y
print(add_numbers(1, 2))
# In[2]:
# Sample addition of three numbers
def add_numbers(x, y, z):
    return x + y + z
print(add_numbers(1, 2, 3))
# In[3]:
# Sample addition of numbers using Python "None"
# This condition allows for calling varibles with null arguments in case of their absence
def add_numbers(x, y, z=None): #var z is defaulted to have no value
       #'if' loop to check for var 'z' value
    if (z==None):
        #if value is not found, only var 'x' and 'y' are added, function is exited
        return x + y
    # if 'z' value is present, adds all three variables
    else:
        return x + y + z
    
print(add_numbers(1, 2))
print(add_numbers(1, 2, 3))
# In[12]:
# how does the boolean 'False' affect this function?
def add_numbers(x, y, z=None, flag=False):
    if (flag): #flag is found so string is printed
        print('Flag is true!')
        
    if (z==None): #'z' value was not passed to function parameters so statement==True; 'if' statement is run.
        return x + y
    
    else: #not returned because 'z' value is not defined
        return x + y + z
print(add_numbers(1, 2, flag=True))
# In[11]:
# function with a flag = false argument
def add_numbers(x, y, z=None, flag=False):
    if (flag):
        print('Flag is true!')
    if (z==None):
        return x + y
    
    else:
        return x + y + z
print(add_numbers(1, 2, flag=False))
# In[19]:
def add_numbers(x, y):
    return x + y
#passes function to the variable 'a'
a = add_numbers
a(1,2)
# In[21]:
#This function should add the two values if the value of the "kind parameter is "add" or is not
#passed in, otherwise it should subtract the second value from the first.
def do_math(a, b , kind='add'):
    if (kind=='add'):
        return a + b
    else:
        return a - b
do_math(1, 2)