#!/usr/bin/env python
# coding: utf-8
# In[25]:
inputs = [0.5, 0.7, 0.1]
goals = [1, 1, 0]
weights = [[0.5,0.7,0.1], [0.1,0.3,0.7], [0.2,0.1,0.1]]
alpha = 0.01
# In[22]:
def neural_network(inputs, weights):
    output = []
    for weight_set in weights:
        output.append(weight_sum(inputs, weight_set))
    return output
def weight_sum(inputs, weights):
    output = 0
    for input, weight in zip(inputs, weights):
        output += (input * weight)
    return output
def element_multiplicaton(inputs, delta):
    output = []
    for input in inputs:
        output.append(input * delta)
    return output
# In[26]:
deltas = [2,4,4]
while sum(map(abs, deltas)) > 0.001 :
    deltas = []
    weight_deltas = []
    preds = neural_network(inputs, weights)
    
    for goal, pred in zip(goals, preds):
        deltas.append(pred - goal)
    
    for delta in deltas:
        weight_deltas.append(element_multiplicaton(inputs, delta))
    for row, weight_delta in enumerate(weight_deltas):
        for col, weight_delta_value in enumerate(weight_delta):
            weights[row][col] -= weight_delta_value * alpha
    print(sum(map(abs, deltas)))