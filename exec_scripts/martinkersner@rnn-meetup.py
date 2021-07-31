#!/usr/bin/env python
# coding: utf-8
# In[1]:
import random
import numpy as np
import tensorflow as tf
def reset_graph(seed=42):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)
# In[2]:
def int2bin(i, length=10):
    b = bin(i)[2:].zfill(length)
    b_lst = [int(i) for i in b]
    b_lst.reverse()
    return np.array(b_lst)
def bin2int(b, axis=0):
    b_lst = list(b[0,:,axis])
    b_lst.reverse()
    b_str = "".join(str(int(i)) for i in b_lst)
    return int(b_str, 2)
def int2binABC(A, B, C, length=10):
    return int2bin(A, length), int2bin(B, length), int2bin(C, length)
def gen_data(func):
    def inner(*args, **kwargs):
        A, B = func(*args, **kwargs)
        C = A+B
        Ab, Bb, Cb = int2binABC(A, B, C)
        X_batch = None
        X_batch = np.vstack((Ab, Bb)).T
        X_batch = X_batch[np.newaxis, :]
        Y_batch = Cb[np.newaxis, :, np.newaxis]
        
        return X_batch, Y_batch
    
    return inner
@gen_data
def gen_given_data(A, B):
    return A, B
@gen_data
def gen_random_data(max_val=100):
    A = np.random.randint(max_val)
    B = np.random.randint(max_val)
    
    return A, B
def gen_dataset(length, binary_length=10):
    X = np.zeros((length*length, binary_length,  2))
    Y = np.zeros((length*length, binary_length, 1))    
    idx = 0
    for A in range(length):
        for B in range(length):
            C = A + B
            Ab, Bb, Cb = int2binABC(A, B, C, binary_length)
            X[idx] = np.vstack((Ab, Bb)).T
            Y[idx] = Cb[:, np.newaxis]
            idx += 1
    return X, Y
def split_train_test(X, Y, ratio=0.7):
    length = X.shape[0]
    
    ran = range(length)
    train_lst = random.sample(ran, int(ratio*length))
    test_lst = list(set(ran)-set(train_lst))
    
    X_train = X[train_lst, :, :]
    Y_train = Y[train_lst, :, :]
    
    X_test = X[test_lst, :, :]
    Y_test = Y[test_lst, :, :]
    return X_train, Y_train, X_test, Y_test
# In[3]:
X_data, Y_data = gen_dataset(100)
X_train, Y_train, X_test, Y_test = split_train_test(X_data, Y_data, 0.10)
# In[4]:
print(X_train.shape[0])
print(X_test.shape[0])
# In[5]:
reset_graph()
n_steps   = 10
n_inputs  = 2
n_outputs = 1
n_neurons = 2
X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])
# RNN cell
cell = tf.contrib.rnn.OutputProjectionWrapper(
    tf.contrib.rnn.BasicRNNCell(num_units=n_neurons),
    output_size=n_outputs)
outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
# In[6]:
learning_rate = 0.01
loss = tf.reduce_mean(tf.square(outputs-y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(loss)
init = tf.global_variables_initializer()
# In[7]:
batch_size   = 50
n_epochs     = 80
saver = tf.train.Saver()
with tf.Session() as sess:
    init.run()
    
    for epoch in range(n_epochs):
        for iteration in range(X_train.shape[0] // batch_size):
            X_batch = X_train[iteration*batch_size:(iteration*batch_size)+batch_size,:,:]
            Y_batch = Y_train[iteration*batch_size:(iteration*batch_size)+batch_size,:,:]
        
            sess.run(training_op, feed_dict={X: X_batch, y: Y_batch})
        mse = loss.eval(feed_dict={X: X_batch, y: Y_batch})
        print("epoch {} MSE: {}".format(epoch, mse))
        
        if mse < 0.01:
            break
    saver.save(sess, "./model")
    
    res = loss.eval(feed_dict={X: X_test, y: Y_test})
    print("test  MSE: ", res)
# In[8]:
A = 853
B = 126
C = A+B
with tf.Session() as sess:
    saver.restore(sess, "./model")
      
    X_batch, y_batch = gen_given_data(A, B)
    
    binary_sum = outputs.eval(feed_dict={X: X_batch, y: y_batch})
    
    # Thresholding is neccessary because predictions from model are floating point values between 0 and 1
    # but we want to obtain binary values.
    binary_sum[binary_sum > 0.5]  = 1
    binary_sum[binary_sum <= 0.5] = 0
    
    int_sum = bin2int(binary_sum)
    
    print("A   ", bin2int(X_batch))
    print("B   ", bin2int(X_batch, axis=1))
    print("SUM ", int_sum)
    
    print("Correct" if C == int_sum else "Wrong")