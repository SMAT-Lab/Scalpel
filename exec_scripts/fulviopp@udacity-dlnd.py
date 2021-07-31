#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
# In[5]:
s = np.array(5)
print(s.shape)
x = s + 3
print(x)
# In[6]:
v = np.array([1,2,3])
print(v.shape)
# In[7]:
values = [1,2,3,4,5]
for i in range(len(values)):
    values[i] += 5
    
print(values)
# In[9]:
values = [1,2,3,4,5]
values = np.array(values) + 5
print(values)
# In[11]:
a = np.array([[1,3],[5,7]])
a
b = np.array([[2,4],[6,8]])
b
a + b
# In[12]:
c = np.array([[2,3,6],[4,5,9],[1,8,7]])
c
# exibe o seguinte resultado:
# array([[2, 3, 6],
#        [4, 5, 9],
#        [1, 8, 7]])
print(a.shape)
# exibe o seguinte resultado:
#  (2, 2)
print(c.shape)
# exibe o seguinte resultado:
#  (3, 3)
# In[15]:
a = np.array([[1,2,3,4],[5,6,7,8]])
a
# exibe o seguinte resultado:
# array([[1, 2, 3, 4],
#        [5, 6, 7, 8]])
a.shape
# exibe o seguinte resultado:
# (2, 4)
b = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
b
# exibe o seguinte resultado:
# array([[ 1,  2,  3],
#        [ 4,  5,  6],
#        [ 7,  8,  9],
#        [10, 11, 12]])
b.shape
# exibe o seguinte resultado:
# (4, 3)
c = np.matmul(a, b)
print(c)
# exibe o seguinte resultado:
# array([[ 70,  80,  90],
#        [158, 184, 210]])
c.shape
# exibe o seguinte resultado:
# (2, 3)
# In[16]:
m = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
m
# exibe o seguinte resultado:
# array([[ 1,  2,  3,  4],
#        [ 5,  6,  7,  8],
#        [ 9, 10, 11, 12]])
# In[17]:
m.T
# In[18]:
inputs = np.array([[-0.27,  0.45,  0.64, 0.31]])
inputs
# exibe o seguinte resultado:
# array([[-0.27,  0.45,  0.64,  0.31]])
# In[19]:
inputs.shape
# In[20]:
weights = np.array([[0.02, 0.001, -0.03, 0.036],     [0.04, -0.003, 0.025, 0.009], [0.012, -0.045, 0.28, -0.067]])
# In[21]:
weights.shape
# In[23]:
np.matmul(inputs, weights.T)
# In[1]:
import pandas as pd
# TODO: Set weight1, weight2, and bias
weight1 = 1.1
weight2 = 1.1
bias = -2.0
# DON'T CHANGE ANYTHING BELOW
# Inputs and outputs
test_inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
correct_outputs = [False, False, False, True]
outputs = []
# Generate and check output
for test_input, correct_output in zip(test_inputs, correct_outputs):
    linear_combination = weight1 * test_input[0] + weight2 * test_input[1] + bias
    output = int(linear_combination >= 0)
    is_correct_string = 'Yes' if output == correct_output else 'No'
    outputs.append([test_input[0], test_input[1], linear_combination, output, is_correct_string])
# Print output
num_wrong = len([output[4] for output in outputs if output[4] == 'No'])
output_frame = pd.DataFrame(outputs, columns=['Input 1', '  Input 2', '  Linear Combination', '  Activation Output', '  Is Correct'])
if not num_wrong:
    print('Nice!  You got it all correct.\n')
else:
    print('You got {} wrong.  Keep trying!\n'.format(num_wrong))
print(output_frame.to_string(index=False))
# In[2]:
# GRADIENT DESCENT
import numpy as np
def sigmoid(x):
    """
    Calculate sigmoid
    """
    return 1/(1+np.exp(-x))
def sigmoid_prime(x):
    """
    # Derivative of the sigmoid function
    """
    return sigmoid(x) * (1 - sigmoid(x))
learnrate = 0.5
x = np.array([1, 2, 3, 4])
y = np.array(0.5)
# Initial weights
w = np.array([0.5, -0.5, 0.3, 0.1])
### Calculate one gradient descent step for each weight
### Note: Some steps have been consilated, so there are
###       fewer variable names than in the above sample code
# TODO: Calculate the node's linear combination of inputs and weights
h = np.dot(x,w)
# TODO: Calculate output of neural network
nn_output = sigmoid(h)
# TODO: Calculate error of neural network
error = y - nn_output
# TODO: Calculate the error term
#       Remember, this requires the output gradient, which we haven't
#       specifically added a variable for.
error_term = error * sigmoid_prime(h)
# TODO: Calculate change in weights
del_w = learnrate * error_term * x
print('Neural Network output:')
print(nn_output)
print('Amount of Error:')
print(error)
print('Change in Weights:')
print(del_w)