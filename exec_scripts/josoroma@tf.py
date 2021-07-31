#!/usr/bin/env python
# coding: utf-8
# In[1]:
ninjas = [
    'Hattori Hanzō',
    'Kumawakamaru',
    'Yagyū Munetoshi',
    'Hattori Hanzō',
    'Ishikawa Goemon',
    'Fūma Kotarō',
    'Mochizuki Chiyome',
    'Momochi Sandayū',
    'Fujibayashi Nagato',
    'Hattori Hanzō'
]
# In[2]:
ninjas
# In[3]:
ninjas.count('Hattori Hanzō')
# In[4]:
ninjas.count('Homma Saburō')
# In[5]:
ninjas.index('Yagyū Munetoshi')
# In[6]:
ninjas.index('Hattori Hanzō')
# In[7]:
ninjas.index('Hattori Hanzō', 1) # Find next ninja starting at position 1
# In[8]:
ninjas.index('Hattori Hanzō', 4) # Find next ninja starting at position 4
# In[9]:
ninjas.reverse()
ninjas
# In[10]:
ninjas.reverse()
ninjas
# In[11]:
ninjas.append('Kamiizumi Ise-no-Kami Nobutsuna')
ninjas
# In[12]:
ninjas.pop()
# In[13]:
ninjas
# In[14]:
ninjas.sort()
    
ninjas
# In[15]:
ninjas = list(set(ninjas))
ninjas
# In[16]:
ninjas.append('Guido van Rossum')
ninjas
ninjas.insert(len(ninjas), 'Guido van Rossum')
ninjas
# In[17]:
ninjas.pop()
ninjas
# In[18]:
from collections import deque
queue = deque([
    'Hattori Hanzō',
    'Fūma Kotarō',
    'Momochi Sandayū'
])
queue
# In[19]:
queue.append('Guido van Rossum')
queue
# In[20]:
queue.popleft()
queue
# In[21]:
ninjas.insert(0, 'Guido van Rossum')
ninjas
# In[22]:
ninjas.pop(0)
ninjas
# In[23]:
quote = "You talkin' to me?".split()
data = list(map(lambda q: [q, q.title(), len(q)], quote))
data
# In[24]:
quote = "You talkin' to me?".split()
data = [
    [
        q, 
        q.title(), 
        len(q)
    ]
    for q in quote
]
data
# In[25]:
numbers = range(1, 11)
odds = [
    n 
    for n in numbers 
    if n % 2 == 0
]
odds
# In[26]:
matrix = [
    [
        1 if item_idx == row_idx else 0 
        for item_idx in range(0, 8)
    ]
    for row_idx in range(0, 8)
]
matrix
# In[27]:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
[[el - 1 for el in row] for row in matrix]
# In[28]:
# Tuples are immutable.
data = (['2016-05-18T16:03:00Z', '2016-05-18T17:20:00Z', '2016-05-18T13:00:00Z'], [100, 2.5, 333])
payments = data[1];
conversion = [float(x) for x in payments]
result = list(zip(data[0], conversion))
result
# In[29]:
# Yep, tuples are immutable.
data = (['2016-05-18T16:03:00Z', '2016-05-18T17:20:00Z', '2016-05-18T13:00:00Z'], [100, 2.5, 333])
# Lists are mutable.
mutable = list(data)
payments = data[1]
mutable[1] = [float(x) for x in payments]
tuples = list(zip(*mutable))
tuples
# In[30]:
numbers = list(range(1, 11))
print(numbers)
del numbers[len(numbers) - 1]
print(numbers)
del numbers[0]
print(numbers)
del numbers[2:4]
print(numbers)
# []
del numbers[:]
print(numbers)
# Delete entire variable.
del numbers
# In[31]:
separated_by_commas = 333, 'three three three', [3, 6, 9], (3 ,6 ,9)
separated_by_commas
separated_by_commas[3]
separated_by_commas[3][2]
# In[32]:
# It is possible to create tuples which contain mutable objects, such as lists.
my_tuple = ('cow', [333, 4, 6], (111, 222, 333))
# my_tuple[0] = 'dog'  =>  'tuple' object does not support item assignment.
my_tuple[1][0] = 2
# my_tuple[2][0] = 2  =>  'tuple' object does not support item assignment.
my_tuple
# In[33]:
first_tuple = 'one', 'two', 'three'
second_tuple = 1, 2, 3
third_tuple = 4.4, 5.5, 6.6
result = first_tuple + second_tuple + third_tuple
result
# In[34]:
# Empty tuples are constructed by an empty pair of parentheses.
empty = ()
print(empty)
print(len(empty))
# In[35]:
# A tuple with one item is constructed by following a value with a comma.
trailing_comma = 333,
print(trailing_comma)
print(len(trailing_comma))
# In[36]:
vehicle = ('Tesla', 'Model 3', 2017)
print(vehicle)
(make, model, year) = vehicle
print(make, type(make))
print(model, type(model))
print(year, type(year))
# In[37]:
# Swap the values of two variables.
min = 10
max = 1
(min, max) = (max, min)
print(min, type(min))
print(max, type(max))
# In[38]:
# Tuples as return values.
def vehicle():
    get_make = 'Tesla'
    get_model = 'Model 3'
    get_year = 2017
    return (get_make, get_model, get_year)
(my_make, my_model, my_year) = vehicle()
print('{} {} {}'.format(my_make, my_model, my_year))
print('{2} {1} {0}'.format(my_make, my_model, my_year))
# In[39]:
# To create an empty set you have to use set(), not {}.
empty_set = set()
print(empty_set)
# In[40]:
chars = set('123,abc,abc,abc,123')
print(chars)
# In[41]:
unique = set([1,2,3,4,5,4,3,2,1])
print(unique)
unordered = {7, 9, 6, 8, 4, 5, 10}
print(unordered)
# In[42]:
# Fast membership testing.
'1' in unique
# In[43]:
1 in unique
# In[44]:
# Fast membership testing.
10 in unordered
# In[45]:
# Numbers in unique but not in unordered.
unique - unordered
# In[46]:
# Numbers in unordered but not in unique.
unordered - unique
# In[47]:
{x for x in unique if x not in [1, 2, 3]}
# In[48]:
numbers = range(1, 11)
print(list(numbers))
print(tuple(numbers))
print(set(numbers))
# In[49]:
numbers = set(range(1, 11))
print(numbers)
# In[50]:
person = {'name': 'Guido van Rossum', 'age': 61, 'occupation': 'Benevolent Dictator For Life'}
print(person['name'])
print(person['age'])
print(person['occupation'])
# In[51]:
print(person)
# In[52]:
values = person.values()
print(values)
# In[53]:
keys = person.keys()
print(keys)
print(sorted(keys))
# In[54]:
items = person.items()
print(items)
# In[55]:
print(list(items))
# In[56]:
items = list(items)
print(items[0])
print(items[1])
print(items[2])
# In[57]:
name = person.get('name')
print(name)
# In[58]:
name = person.get('username', 'default')
print(name)
# In[59]:
'age' in person
# In[60]:
'username' in person
# In[61]:
person['occupation'] = 'Author of Python'
print(person)
# In[62]:
person = dict(
    [
        ('name', 'Guido van Rossum'), 
        ('age', 61), 
        ('occupation', 'Benevolent Dictator For Life')
    ]
)
print(person)
# In[63]:
keys = ['name', 'age', 'occupation']
values = ['Guido van Rossum', 61, 'Author of Python']
print(keys)
print(values)
# In[64]:
dictionary = dict(zip(keys, values))
print(dictionary)
# In[65]:
# Dictionary Comprehension.
dictionary = { k:v for (k,v) in zip(keys, values)}
print(dictionary)
# In[66]:
d = {'a':1,'b':2,'c':3}
d = {k: v for (k, v) in d.items() if v > 2}
print(d)
# In[67]:
d = {'a':1,'b':2,'c':3}
d = {k + 'c': v * 2 for (k, v) in d.items() if v > 2}
print(d)
# In[68]:
user = {'name': 'Guido van Rossum', 'website': 'https://gvanrossum.github.io/'}
defaults = {'name': "Benevolent Dictator For Life", 'page_name': 'Personal Home Page'}
context = {**defaults, **user}
print(context)
# In[69]:
game = enumerate(['tic', 'tac', 'toe'])
print(list(game))
# In[70]:
# Through a sequence.
game = enumerate(['tic', 'tac', 'toe'])
for i, v in game:
    print(i, v)
# In[71]:
# Over two or more sequences at the same time.
questions = ['What is your name', 'What do you do', 'What would you like to drink']
answers = ['Guido van Rossum', 'A Benevolent Dictator For Life', 'Beer']
# The entries can be paired with the zip() function.
for q, a in zip(questions, answers):
    print('What is your {0}? {1}.'.format(q, a))
# In[72]:
group = {'Animalia': 'Linnaeus', 'Plantae': 'Haeckel', 'Fungi': 'Whittaker', 'Bacteria' : 'Cavalier-Smith'}
for k, v in group.items():
    print(k, ' => ', v)
# In[73]:
kingdoms = ['Bacteria', 'Archaea', 'Protozoa', 'Chromista', 'Plantae', 'Fungi', 'Animalia']
for f in sorted(set(kingdoms)):
    print(f)
# In[74]:
import math
raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
print(raw_data)
filtered_data = []
for value in raw_data:
    if not math.isnan(value):
        filtered_data.append(value)
print(filtered_data)
print(sorted(filtered_data))
# In[75]:
string1, string2, string3 = '', 'Guido', 'van Rossum'
non_null = string1
print(' string1 => ', non_null)
non_null = string2
print(' string2 => ', non_null)
non_null = string1 or string2
print(' string1 or string2 => ', non_null)
non_null = string1 or string2 or string3
print(' string1 or string2 or string3 => ', non_null)
# In[76]:
(1, 2, 3) < (1, 2, 4)
# In[77]:
(1, 2, 5) < (1, 2, 4)
# In[78]:
[1, 2, 3] < [1, 2, 4]
# In[79]:
[1, 2, 5] < [1, 2, 4]
# In[80]:
'ABC' < 'A'
# In[81]:
'ABC' < 'B'
# In[82]:
'ABC' < 'C'
# In[83]:
'ABC' < 'C' < 'Pascal' < 'Python'
# In[84]:
(1, 2) < (1, 2, -1)
# In[85]:
(1, 2, 3) == (1.0, 2.0, 3.0)
# In[86]:
(1, 2, ('aa', 'ab')) < (1, 2, ('abc', 'a'), 4)