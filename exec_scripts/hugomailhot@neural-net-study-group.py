#!/usr/bin/env python
# coding: utf-8
# In[17]:
import tensorflow as tf
import pickle
import matplotlib.pyplot as plt
import numpy as np
# In[18]:
with open('../datasets/scatter.pickle', 'rb') as f:
    data = pickle.load(f)
    x_vals = [x for x in data[0]]
    y_vals = [x for x in data[1]]
# In[19]:
plt.scatter(x_vals, y_vals)
plt.show()
# In[20]:
x_data = tf.placeholder(shape=[None, 1], dtype=tf.float32)
y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)
a = tf.Variable(tf.random_normal(shape=[1,1]))
b = tf.Variable(tf.random_normal(shape=[1,1]))
init = tf.global_variables_initializer()
# In[21]:
model_output = tf.add(tf.matmul(x_data, a), b)
# In[22]:
loss = tf.reduce_mean(tf.square(y_target - model_output))
learning_rate = 0.0001
batch_size = 25
my_opt = tf.train.GradientDescentOptimizer(learning_rate)
train_step = my_opt.minimize(loss)
# In[23]:
sess = tf.Session()
sess.run(init)
# In[24]:
loss_vec = []
for i in range(100):
    rand_index = np.random.choice(len(x_vals), size=batch_size)
    rand_x = np.transpose([[x_vals[i] for i in rand_index]])
    rand_y = np.transpose([[y_vals[i] for i in rand_index]])
    sess.run(train_step, feed_dict={x_data: rand_x, y_target: rand_y})
    temp_loss = sess.run(loss, feed_dict={x_data: rand_x, y_target: rand_y})
    loss_vec.append(temp_loss)
    if (i+1)%10 == 0:
        print('Step #' + str(i+1) + ' A = ' + str(sess.run(a)) 
              + 'b = ' + str(sess.run(b)))
        print('Loss = ''' + str(temp_loss))
# In[25]:
# Make default plot size larger
import matplotlib
matplotlib.rcParams['figure.figsize'] = [12,8]
plt.plot(range(1,101), loss_vec)
plt.ylabel('Loss')
plt.xlabel('Training iterations')
plt.tight_layout()
plt.show()
# In[41]:
# This is how you access a value in a ndarray from numpy
sess.run(a).item()
# In[27]:
# In[42]:
predicted_y_values = [sess.run(a).item() * x + sess.run(b).item() for x in x_vals]
plt.scatter(x_vals, y_vals, color='b')
plt.plot(x_vals, predicted_y_values, color='r')
plt.show()