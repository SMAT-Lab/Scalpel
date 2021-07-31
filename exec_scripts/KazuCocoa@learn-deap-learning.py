#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pylab as plt
# In[2]:
def step_function(x):
    if x > 0:
        return 1
    else:
        return 0
# In[3]:
def step_function2(x):
    return np.array(x > 0, dtype=np.int)
# In[4]:
def step_graph():
    x = np.arange(-5.0, 5.0, 0.1)
    y = step_function2(x)
    plt.plot(x, y)
    plt.ylim(-0.1, 1.1)
    plt.show()
# In[5]:
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
# In[8]:
def sigmoid_graph():
    x = np.arange(-5.0, 5.0, 0.1)
    y = sigmoid(x)
    plt.plot(x, y)
    plt.ylim(-0.1, 1.1)
    plt.show()
# In[9]:
sigmoid_graph()
# In[12]:
A = np.array([[1,2], [3,4]])
A.shape
# In[13]:
B = np.array([[5,6], [7,8]])
B.shape
# In[14]:
np.dot(A, B) # 内積、ドット積
# In[42]:
# start init_network
# In[15]:
X = np.array([1.0, 0.5])
# In[16]:
W1 = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]])
# In[17]:
B1 = np.array([0.1, 0.2, 0.3])
# In[21]:
W1.shape
# In[19]:
X.shape
# In[20]:
B1.shape
# In[22]:
A1 = np.dot(X, W1) + B1
# In[23]:
print(A1)
# In[24]:
Z1 = sigmoid(A1)
# In[43]:
print(Z1)
# In[26]:
W2 = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
# In[27]:
B2 = np.array([0.1, 0.2])
# In[30]:
Z1.shape
# In[29]:
W2.shape
# In[31]:
B2.shape
# In[32]:
A2 = np.dot(Z1, W2) + B2
# In[33]:
Z2 = sigmoid(A2)
# In[34]:
print(A2)
# In[35]:
print(Z2)
# In[36]:
def identity_function(x):
    return x
# In[37]:
W3 = np.array([[0.1, 0.3], [0.2, 0.4]])
# In[38]:
B3 = np.array([0.1, 0.2])
# In[39]:
A3 = np.dot(Z2, W3) + B3
# In[40]:
Y = identity_function(A3)
# In[41]:
print(Y)