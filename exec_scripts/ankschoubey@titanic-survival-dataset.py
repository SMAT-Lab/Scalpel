#!/usr/bin/env python
# coding: utf-8
# In[32]:
from pandas import *
import numpy
# In[33]:
df = read_csv('test.csv')
# In[37]:
survival = []
number = []
# In[38]:
for index, passenger in df.iterrows():
    id = passenger['PassengerId']
    number.append(id)
    if passenger['Sex'] == 'male':
            prediction = 0
    else:
        if passenger['Pclass'] != 3 or passenger['SibSp'] == 0 and passenger['Parch'] ==0:
            prediction = 1
        else:
            prediction = 0
            
    survival.append(prediction)
# In[42]:
output = DataFrame({'PassengerID': number, 'Survived': survival})
output.to_csv('result.csv', index=False)