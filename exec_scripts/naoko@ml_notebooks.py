#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
# In[2]:
X = np.array([
    [0, 0, 1],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
])
y = np.array([[0], [1], [1], [0]])
# In[3]:
print("Input\n{}\n\nOutput\n{}".format(X, y))
# In[4]:
# Set Hyperparameter
num_epoches = 60000
# In[5]:
# Initialize weights with Normal Distribution with low variation
# values will be -1 < weight values < 1
syn0 = 2 * np.random.random((X.shape[1], X.shape[0])) - 1
syn1 = 2 * np.random.random((y.shape[0], y.shape[1])) - 1
print(syn0)
# In[6]:
def deriv(x):
    """returns derivative of x"""
    return x * (1-x)
def sigmoid(x):
    """squash x and returns value between 0 and 1"""
    return 1 / (1 + np.exp(-x))
# In[7]:
for j in range(num_epoches):
    # feed forward through layers 0, 1 and 2
    l0 = X
    l1 = sigmoid(np.dot(l0, syn0))
    l2 = sigmoid(np.dot(l1, syn1))
    
    # CALCULATE ERROR
    # how much did we miss the target value?
    # minimize error over time by changing weights
    l2_error = y - l2
    
    if j % 10000 == 0:
        print("Error: {}".format(np.mean(np.abs(l2_error))))
    
    # BACKPROPAGATE
    # in what direction is the target value?
    # l2_delta = error weighted derivative
    # delta = change
    l2_delta = l2_error * deriv(l2)
    
    # how much did each l1 value contribute to l2 error?
    l1_error = l2_delta.dot(syn1.T)
    
    l1_delta = l1_error * deriv(l1)
    
    # update weights (CORRECT COST)
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)
    