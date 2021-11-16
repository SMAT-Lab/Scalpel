#!/usr/bin/env python
# coding: utf-8
# In[1]:
from bayespy.nodes import Categorical, Beta, Mixture
lambda1 = Beta([20,5]) 
lambda2 = Beta([[5,20],[20,5]])
theta1 = Categorical(lambda1)
theta2 = Mixture(theta1, Categorical, lambda2)
pi1 = Beta([[[5,20], [20,5]]], plates=(10,2))
pi2 = Beta([[[5,20], [20,5]]], plates=(10,2))
pi3 = Beta([[[5,20], [20,5]]], plates=(10,2))
# In[2]:
from bayespy.nodes import Bernoulli, Take
X1 = Mixture(theta1, Bernoulli, pi1)
X2 = Mixture(theta2, Bernoulli, pi2)
X3 = Mixture(theta1, Mixture, theta2, Bernoulli, Take(pi3, [[0, 0], [0, 1]]))
X1.observe([0,1,0,1,0,1,0,1,0,1])
X2.observe([0,1,0,1,0,1,0,1,0,1])
X3.observe([1,1,1,1,1,1,1,1,1,1])
# In[3]:
from bayespy.inference import VB
Q = VB(X1, X2, X3, pi1, pi2, pi3, theta2, theta1, lambda1, lambda2)
Q.update(repeat=100)
print(theta1.get_moments()[0])
print(theta2.get_moments()[0])
# In[4]:
v1 = Categorical([0.5, 0.5])
v2 = Categorical([0.5, 0.5])
v3 = Mixture(v1, Mixture, v2, Categorical,
             [[[0.9,0.1], [0.1,0.9]],
              [[0.1,0.9], [0.9,0.1]]])
v3.observe(1)
# In[5]:
v1.initialize_from_random()
v2.initialize_from_random()
Q = VB(v1, v2, v3)
Q.update(repeat=100, verbose=False)
print(v1.get_moments()[0])
print(v2.get_moments()[0])
# In[13]:
print(np.mean(Bernoulli(Beta([20, 5]), plates=(100000,)).random()))
print(np.mean(Bernoulli(Beta([200, 50]), plates=(100000,)).random()))
print(np.mean(Bernoulli(Beta([20000, 5000]), plates=(100000,)).random()))
print(np.mean(Bernoulli(Beta([2000000, 500000]), plates=(100000,)).random()))