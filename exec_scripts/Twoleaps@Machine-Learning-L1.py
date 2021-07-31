#!/usr/bin/env python
# coding: utf-8
# In[1]:
"""
This notebook presents a primer on Python.
We have tried to cover all the required parts of Python programming language which will be useful in the final project.
However, we have refrained from entering into advanced python concepts since that diverges our focus from the main goal.
Topics are covered in a logical sequence. 
Feel free to comment and ask questions.
Together, we shall conquer this.
"""
# In[3]:
# Python: A general Overview
"""
Python is designed by Guido van Rossum, a dutch Programmer.
It's name is derived from the television series Monty Python's Flying Circus.
It is one of the most widely used languages in the world.
Python is a dynamically typed,  byte code interpreted, object oriented language language.
Python has one of the richest arsenal of data-science and machine learning libraries.
"""
# In[15]:
# Python variable declaration and assignment
tv_series     =  "Monty Python"
"""
^                 ^
|                 |
Varibale Name    Value
In the above example *tv_series* is the variable name and *Monty Python* is its value
In Python all the value on the right hand side of the equality (RValues) are object.
We do not assign variables to any value instread we just give names to objects.
Hence same variable can be assigned to different values (objects)
"""
tv_series = "Game of Thrones"             # again a string
tv_series = 7                             # changed to int
tv_series = False                         # changed to boolean
tv_series = ["Game of Thrones", 7, False] # changed to list
"""
tv_series variable has been assigned values(objects) of 4 differet types 
"""
# In[18]:
# Python Built-in data types
"""
Numeric types
1. int 
3. float
4. complex
"""
numeric_value = 10           # assigned an int
numerec_value = 10.11        # re-assigned as float
numeric_value = 10.11j       # re-assigned as complex number 
# In[19]:
# TO DO
"""
declare a varible num and assign it None
1. change its value to an integer
2. change its value to a float value
3. change its vale to a complex number (if you append j at the end of )
"""
# YOUR CODE STARTS
a = None
# YOUR CODE ENDS