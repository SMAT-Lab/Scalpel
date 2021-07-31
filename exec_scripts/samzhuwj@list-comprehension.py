#!/usr/bin/env python
# coding: utf-8
# In[1]:
# Iterating through string 'human'
h_letters = []
for letter in 'human':
    h_letters.append(letter)
print(h_letters)
# In[3]:
# Use list comprehension
# Syntax of list comprehension: [expression for item in list]
h_letters = [ letter for letter in 'human' ]
print( h_letters)
# In[6]:
# Use Lambda functions
h_letters = list(map(lambda x: x, 'human'))
print( h_letters)
# In[7]:
# Get even numbers from range() by using if
number_list = [ x for x in range(20) if x % 2 == 0]
print(number_list)
# In[8]:
# Get numbers divisible by 2 and 5 from range() using nested if
num_list = [y for y in range(100) if y % 2 == 0 if y % 5 == 0]
print(num_list)
# In[9]:
# List comprehension using if else
obj = ["Even" if i%2==0 else "Odd" for i in range(10)]
print(obj)
# In[17]:
# Find transpose of matrix using nested loops
matrix = [[1, 2],[3,4],[5,6],[7,8]]
transpose = [[row[i] for row in matrix] for i in range(2)]
print (transpose)
# In[20]:
matrix = [[1, 2],[3,4],[5,6],[7,8]]
transposed = []
for i in range(2):
    transposed_row = []
    for row in matrix:
        transposed_row.append(row[i])    
    transposed.append(transposed_row)
print(transposed)