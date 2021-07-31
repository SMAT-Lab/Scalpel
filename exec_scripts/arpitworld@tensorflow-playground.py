#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import math
# In[2]:
ratings_df = pd.read_csv('blog.csv', header=None)
print(len(ratings_df))    # Let's see how many rows we have
ratings_df.head()         # Let's print first few rows
# In[3]:
ratings_df.columns = ['UserId', 'StoryId', 'Rating']
ratings_df.head()
# In[4]:
y_df = ratings_df.pivot_table(index=['StoryId'], columns=['UserId'])
y = np.array(y_df)
y_bool = np.where(np.isnan(y), 0, 1).astype(bool)
y_map = np.where(np.isnan(y), 0, y)
# In[5]:
M,K = y_map.shape
N = 20
print(M,'Stories')
print(N,'Features')
print(K,'Users')
# In[6]:
r = np.random.random([M,K])
y_train_bool = tf.to_float(y_bool * np.greater(r,0.3))
y_test_bool = tf.to_float(y_bool * np.greater(0.3, r))
# In[7]:
x = tf.Variable(tf.random_uniform([M,N]))/100
# In[8]:
w = tf.Variable(tf.random_uniform([N, K]))/100
b = tf.Variable(tf.random_uniform([K]))/100
# In[9]:
h = tf.matmul(x,w) + b
# In[10]:
lambda_ = tf.to_float(2.5)
# In[11]:
cost_function = (
    (0.5)*tf.reduce_sum(y_train_bool * tf.square(h-y_map)) + \
    (lambda_/2)*tf.reduce_sum(tf.square(x)) + \
    (lambda_/2)*tf.reduce_sum(tf.square(w))
) 
# In[12]:
cost_function_test =  (
  (0.5)*tf.reduce_sum(y_test_bool*tf.square(h-y_map))
)
# In[13]:
alpha = tf.placeholder(tf.float32)  # Learning Rate
training_step = tf.train.AdamOptimizer(alpha).minimize(cost_function)
# In[14]:
# init
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
# In[15]:
plot_data = {'c_test' : [], 'c_train' : []}
iters = 1000
for i in range(iters):
    # Exponentially decay learning rate
    max_learning_rate = 1
    min_learning_rate = 0.1
    decay_speed = 50
    learning_rate = min_learning_rate +     (max_learning_rate - min_learning_rate) * math.exp(-i/decay_speed)
    # Optimize
    _, c, ct = sess.run([training_step, cost_function, cost_function_test], {alpha: learning_rate})
    
    # Store cost function for each iteration
    plot_data['c_train'].append(c)
    plot_data['c_test'].append(ct)
    
    # Print occasionally to see progress
    if i%20==0:
        print(i, c, ct)
print("Training Complete")
# In[16]:
# Plotting Training Error Chart
plt.plot(range(iters), plot_data['c_train'])
plt.show()
# In[17]:
# Plotting Testing Error Chart
plt.plot(range(iters), plot_data['c_test'])
plt.show()
# In[18]:
evaluated_y_test_bool, predicted = sess.run([y_test_bool, h])
evaluated_y_test_bool = evaluated_y_test_bool.astype(bool)
predicted = predicted*evaluated_y_test_bool
real = y_map*evaluated_y_test_bool
predicted = predicted[predicted.nonzero()]
real = real[real.nonzero()]
yi = np.lexsort((predicted, real))
predicted, real = predicted[yi], real[yi]
plt.plot(range(len(predicted)), predicted)
plt.plot(range(len(real)), real)
plt.show()