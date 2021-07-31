#!/usr/bin/env python
# coding: utf-8
# In[1]:
import csv
# In[2]:
def readEpochData(file):
    """
    Reads the epoch lost data from a csv file.
    """
    epochs = []
    with open(file) as dataFile:
        dataReader = csv.reader(dataFile)
        for row in dataReader:
            batch = []
            for value in row:
                batch.append(float(value))
            epochs.append(batch)
        
    return epochs
    
epoch6 = readEpochData('../data/EpochData/Epoch6.csv')
# In[3]:
import matplotlib.pyplot as plt
import numpy as np
# Visualizations will be shown in the notebook.
get_ipython().run_line_magic('matplotlib', 'inline')
# In[4]:
def showEpoch(epochs, title):
    """
    Display epoch data.
    """
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.violinplot(epochs, showmeans=True)
    ax.yaxis.grid(True)
    ax.set_xticks([y+1 for y in range(len(epochs))])
    ax.set_xlabel('Epochs')
    ax.set_ylabel('Loss')
    ax.set_title(title)
    plt.show()
showEpoch(epoch6, '6 Epochs')
# In[5]:
epoch12 = readEpochData('../data/EpochData/Epoch12.csv')
showEpoch(epoch12, '12 Epochs')
# In[6]:
epoch24 = readEpochData('../data/EpochData/Epoch24.csv')
showEpoch(epoch24, '24 Epochs')
# In[7]:
epoch48 = readEpochData('../data/EpochData/Epoch48.csv')
showEpoch(epoch48, '48 Epochs')
# In[8]:
def showLastEpochLoss(title, data):
    """
    Prints the last epoch mean and standard deviation.
    """
    last = data[-1]
    print(title);
    print('   Mean: {:3f}'.format(np.mean(last)))
    print('   Std: {:3f}'.format(np.std(last)))
    print()
showLastEpochLoss('6 Epoch', epoch6)
showLastEpochLoss('12 Epoch', epoch12)
showLastEpochLoss('24 Epoch', epoch24)
showLastEpochLoss('48 Epoch', epoch48)