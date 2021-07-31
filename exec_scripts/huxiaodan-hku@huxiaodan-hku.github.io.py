#!/usr/bin/env python
# coding: utf-8
# In[1]:
from __future__ import print_function, division
import numpy as np
import tensorflow as tf
# In[2]:
num_epochs = 5   #全部数据一共反复训练次数
total_series_length = 50000   
truncated_backprop_length = 10     #输入X1,x2,...Xn 的长度
state_size = 4     #隐藏层大小
num_classes = 2     #输出的class ， 本程序只有0,1两种输出
echo_step = 3      #输出偏移位数
batch_size = 5     #batch_sizs
num_layers = 3     #多层隐藏层
num_batches = total_series_length//batch_size//truncated_backprop_length    #batch 的数量
# In[3]:
inputs_value = np.array(np.random.choice(2, total_series_length, p=[0.5, 0.5]))
targets_value = np.roll(inputs_value, echo_step)
for i in range(num_batches * batch_size):
    targets_value[i * truncated_backprop_length : (i * truncated_backprop_length + echo_step)] = 0
inputs_value = inputs_value.reshape((batch_size, -1))  
targets_value = targets_value.reshape((batch_size, -1))
# In[4]:
batchX_placeholder = tf.placeholder(tf.int32, [batch_size, truncated_backprop_length])
batchY_placeholder = tf.placeholder(tf.int32, [batch_size, truncated_backprop_length])
#one_hot_batchX_placeholder = tf.one_hot(batchX_placeholder,num_classes)
with tf.variable_scope("embedding",reuse=tf.AUTO_REUSE):
    embeddings = tf.get_variable('embedding_matrix', [num_classes, state_size])
rnn_inputs = tf.nn.embedding_lookup(embeddings, batchX_placeholder)
# In[5]:
lstm_cell = tf.contrib.rnn.BasicLSTMCell(state_size,state_is_tuple=True)
lstm_cell = tf.contrib.rnn.MultiRNNCell([lstm_cell] * num_layers, state_is_tuple=True)
init_state = lstm_cell.zero_state(batch_size, tf.float32)
rnn_outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, rnn_inputs, initial_state=init_state)
# In[7]:
W2 = tf.Variable(np.random.rand(state_size, num_classes),dtype=tf.float32)
b2 = tf.Variable(np.zeros((1,num_classes)), dtype=tf.float32)
logits = tf.reshape(
            tf.matmul(tf.reshape(rnn_outputs, [-1, state_size]), W2) + b2,
            [batch_size, truncated_backprop_length, num_classes])
losses = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=batchY_placeholder, logits=logits)
total_loss = tf.reduce_mean(losses)
train_step = tf.train.AdagradOptimizer(0.3).minimize(total_loss)
# In[8]:
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    loss_list = []
    for epoch_idx in range(num_epochs):
        _current_cell_state = np.zeros((batch_size, state_size))
        _current_hidden_state = np.zeros((batch_size, state_size))
        print("New data, epoch", epoch_idx)
        for batch_idx in range(num_batches):
            start_idx = batch_idx * truncated_backprop_length
            end_idx = start_idx + truncated_backprop_length
            batchX = inputs_value[:,start_idx:end_idx]
            batchY = targets_value[:,start_idx:end_idx]
            _total_loss, _train_step = sess.run(
                [total_loss, train_step],
                feed_dict={
                    batchX_placeholder: batchX,
                    batchY_placeholder: batchY,
                })
            loss_list.append(_total_loss)
            if batch_idx%100 == 0:
                print("Step",batch_idx, "Batch loss", _total_loss)