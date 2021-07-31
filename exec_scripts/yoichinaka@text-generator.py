#!/usr/bin/env python
# coding: utf-8
# In[1]:
### Load in necessary libraries for data input and normalization
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
from my_answers import *
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
from my_answers import *
### load in and normalize the dataset
dataset = np.loadtxt('datasets/normalized_apple_prices.csv')
# In[2]:
# lets take a look at our time series
plt.plot(dataset)
plt.xlabel('time period')
plt.ylabel('normalized series value')
# In[3]:
odd_nums = np.array([1,3,5,7,9,11,13])
# In[4]:
# run a window of size 2 over the odd number sequence and display the results
window_size = 2
X = []
X.append(odd_nums[0:2])
X.append(odd_nums[1:3])
X.append(odd_nums[2:4])
X.append(odd_nums[3:5])
X.append(odd_nums[4:6])
y = odd_nums[2:]
X = np.asarray(X)
y = np.asarray(y)
y = np.reshape(y, (len(y),1)) #optional
assert(type(X).__name__ == 'ndarray')
assert(type(y).__name__ == 'ndarray')
assert(X.shape == (5,2))
assert(y.shape in [(5,1), (5,)])
# print out input/output pairs --> here input = X, corresponding output = y
print ('--- the input X will look like ----')
print (X)
print ('--- the associated output y will look like ----')
print (y)
# In[5]:
### TODO: implement the function window_transform_series in the file my_answers.py
from my_answers import window_transform_series
# In[6]:
# window the data using your windowing function
window_size = 7
X,y = window_transform_series(series = dataset,window_size = window_size)
# In[7]:
# split our dataset into training / testing sets
train_test_split = int(np.ceil(2*len(y)/float(3)))   # set the split point
# partition the training set
X_train = X[:train_test_split,:]
y_train = y[:train_test_split]
# keep the last chunk for testing
X_test = X[train_test_split:,:]
y_test = y[train_test_split:]
# NOTE: to use keras's RNN LSTM module our input must be reshaped to [samples, window size, stepsize] 
X_train = np.asarray(np.reshape(X_train, (X_train.shape[0], window_size, 1)))
X_test = np.asarray(np.reshape(X_test, (X_test.shape[0], window_size, 1)))
# In[8]:
### TODO: create required RNN model
# import keras network libraries
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras
# given - fix random seed - so we can all reproduce the same results on our default time series
np.random.seed(0)
# TODO: implement build_part1_RNN in my_answers.py
from my_answers import build_part1_RNN
model = build_part1_RNN(window_size)
# build model using keras documentation recommended optimizer initialization
optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
# compile the model
model.compile(loss='mean_squared_error', optimizer=optimizer)
# In[51]:
# run your model!
model.fit(X_train, y_train, epochs=1000, batch_size=50, verbose=0)
# In[52]:
# generate predictions for training
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)
# In[53]:
# print out training and testing errors
training_error = model.evaluate(X_train, y_train, verbose=0)
print('training error = ' + str(training_error))
testing_error = model.evaluate(X_test, y_test, verbose=0)
print('testing error = ' + str(testing_error))
# In[35]:
### Plot everything - the original series as well as predictions on training and testing sets
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# plot original series
plt.plot(dataset,color = 'k')
# plot training set prediction
split_pt = train_test_split + window_size 
plt.plot(np.arange(window_size,split_pt,1),train_predict,color = 'b')
# plot testing set prediction
plt.plot(np.arange(split_pt,split_pt + len(test_predict),1),test_predict,color = 'r')
# pretty up graph
plt.xlabel('day')
plt.ylabel('(normalized) price of Apple stock')
plt.legend(['original series','training fit','testing fit'],loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
# In[9]:
# read in the text, transforming everything to lower case
text = open('datasets/holmes.txt').read().lower()
print('our original text has ' + str(len(text)) + ' characters')
# In[10]:
### print out the first 1000 characters of the raw text to get a sense of what we need to throw out
text[:2000]
# In[11]:
### find and replace '\n' and '\r' symbols - replacing them 
text = text[1302:]
text = text.replace('\n',' ')    # replacing '\n' with '' simply removes the sequence
text = text.replace('\r',' ')
# In[12]:
### print out the first 1000 characters of the raw text to get a sense of what we need to throw out
text[:1000]
# In[13]:
### TODO: implement cleaned_text in my_answers.py
from my_answers import cleaned_text
text = cleaned_text(text)
# shorten any extra dead space created above
text = text.replace('  ',' ')
# In[14]:
### print out the first 2000 characters of the raw text to get a sense of what we need to throw out
text[:2000]
# In[15]:
# count the number of unique characters in the text
chars = sorted(list(set(text)))
# print some of the text, as well as statistics
print ("this corpus has " +  str(len(text)) + " total number of characters")
print ("this corpus has " +  str(len(chars)) + " unique characters")
# In[16]:
### TODO: implement window_transform_series in my_answers.py
from my_answers import window_transform_series
# In[17]:
# run your text window-ing function 
window_size = 100
step_size = 5
inputs, outputs = window_transform_text(text,window_size,step_size)
# In[18]:
# print out a few of the input/output pairs to verify that we've made the right kind of stuff to learn from
print('input = ' + inputs[2])
print('output = ' + outputs[2])
print('--------------')
print('input = ' + inputs[100])
print('output = ' + outputs[100])
# In[19]:
# print out the number of unique characters in the dataset
chars = sorted(list(set(text)))
print ("this corpus has " +  str(len(chars)) + " unique characters")
print ('and these characters are ')
print (chars)
# In[20]:
# this dictionary is a function mapping each unique character to a unique integer
chars_to_indices = dict((c, i) for i, c in enumerate(chars))  # map each unique character to unique integer
# this dictionary is a function mapping each unique integer back to a unique character
indices_to_chars = dict((i, c) for i, c in enumerate(chars))  # map each unique integer back to unique character
# In[21]:
# transform character-based input/output into equivalent numerical versions
def encode_io_pairs(text,window_size,step_size):
    # number of unique chars
    chars = sorted(list(set(text)))
    num_chars = len(chars)
    
    # cut up text into character input/output pairs
    inputs, outputs = window_transform_text(text,window_size,step_size)
    
    # create empty vessels for one-hot encoded input/output
    X = np.zeros((len(inputs), window_size, num_chars), dtype=np.bool)
    y = np.zeros((len(inputs), num_chars), dtype=np.bool)
    
    # loop over inputs/outputs and transform and store in X/y
    for i, sentence in enumerate(inputs):
        for t, char in enumerate(sentence):
            X[i, t, chars_to_indices[char]] = 1
        y[i, chars_to_indices[outputs[i]]] = 1
        
    return X,y
# In[22]:
# use your function
window_size = 100
step_size = 5
X,y = encode_io_pairs(text,window_size,step_size)
# In[23]:
### necessary functions from the keras library
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import keras
import random
# TODO implement build_part2_RNN in my_answers.py
from my_answers import build_part2_RNN
model = build_part2_RNN(window_size, len(chars))
# initialize optimizer
optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
# compile model --> make sure initialized optimizer and callbacks - as defined above - are used
model.compile(loss='categorical_crossentropy', optimizer=optimizer)
# In[24]:
# a small subset of our input/output pairs
Xsmall = X[:10000,:,:]
ysmall = y[:10000,:]
# In[21]:
# train the model
model.fit(Xsmall, ysmall, batch_size=500, epochs=40,verbose = 1)
# save weights
model.save_weights('model_weights/best_RNN_small_textdata_weights.hdf5')
# In[25]:
# function that uses trained model to predict a desired number of future characters
def predict_next_chars(model,input_chars,num_to_predict):     
    # create output
    predicted_chars = ''
    for i in range(num_to_predict):
        # convert this round's predicted characters to numerical input    
        x_test = np.zeros((1, window_size, len(chars)))
        for t, char in enumerate(input_chars):
            x_test[0, t, chars_to_indices[char]] = 1.
        # make this round's prediction
        test_predict = model.predict(x_test,verbose = 0)[0]
        # translate numerical prediction back to characters
        r = np.argmax(test_predict)                           # predict class of each test input
        d = indices_to_chars[r] 
        # update predicted_chars and input
        predicted_chars+=d
        input_chars+=d
        input_chars = input_chars[1:]
    return predicted_chars
# In[26]:
# TODO: choose an input sequence and use the prediction function in the previous Python cell to predict 100 characters following it
# get an appropriately sized chunk of characters from the text
start_inds = [i for i in range(0, 1000, 100)]
# load in weights
model.load_weights('model_weights/best_RNN_small_textdata_weights.hdf5')
for s in start_inds:
    start_index = s
    input_chars = text[start_index: start_index + window_size]
    # use the prediction function
    predict_input = predict_next_chars(model,input_chars,num_to_predict = 100)
    # print out input characters
    print('------------------')
    input_line = 'input chars = ' + '\n' +  input_chars + '"' + '\n'
    print(input_line)
    # print out predicted characters
    line = 'predicted chars = ' + '\n' +  predict_input + '"' + '\n'
    print(line)
# In[27]:
### A simple way to write output to file
f = open('my_test_output.txt', 'w')              # create an output file to write too
f.write('this is only a test ' + '\n')           # print some output text
x = 2
f.write('the value of x is ' + str(x) + '\n')    # record a variable value
f.close()     
# print out the contents of my_test_output.txt
f = open('my_test_output.txt', 'r')              # create an output file to write too
f.read()
# In[28]:
# TODO: choose an input sequence and use the prediction function in the previous Python cell to predict 100 characters following it
# get an appropriately sized chunk of characters from the text
start_inds = [i for i in range(0, 1000, 100)]
# save output
f = open('text_gen_output/RNN_large_textdata_output.txt', 'w')  # create an output file to write too
# load weights
model.load_weights('model_weights/best_RNN_large_textdata_weights.hdf5')
for s in start_inds:
    start_index = s
    input_chars = text[start_index: start_index + window_size]
    # use the prediction function
    predict_input = predict_next_chars(model,input_chars,num_to_predict = 100)
    # print out input characters
    line = '-------------------' + '\n'
    print(line)
    f.write(line)
    input_line = 'input chars = ' + '\n' +  input_chars + '"' + '\n'
    print(input_line)
    f.write(input_line)
    # print out predicted characters
    predict_line = 'predicted chars = ' + '\n' +  predict_input + '"' + '\n'
    print(predict_line)
    f.write(predict_line)
f.close()