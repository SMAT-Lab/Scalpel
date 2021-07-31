#!/usr/bin/env python
# coding: utf-8
# In[126]:
# get useful libraries for data exploration
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# In[127]:
# get csv data 
with open("mnist_dataset/mnist_train_100.csv") as f:
    data = f.readlines()
# In[128]:
# looking at a data entry
data[0]
# In[129]:
# convert each line of csv text into lists of individual values
all_values_mine = [line.rstrip().split(",") for line in data] # rstrip to get rid of the newline character
# In[130]:
# helper function that changes a list of pixels into an image array 
def transform(pixel_list):
    return np.array(pixel_list).reshape((28, 28))
# In[132]:
# convert text to real numbers for all values (except for the target) 
image_pixels = np.asfarray([transform(image[1:]) for image in all_values_mine])
#print(type(image_pixels[0][0]))
plt.imshow(image_pixels[99], cmap='Greys', interpolation='None')