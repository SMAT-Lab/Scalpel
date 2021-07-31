#!/usr/bin/env python
# coding: utf-8
# In[6]:
get_ipython().run_line_magic('matplotlib', 'inline')
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
def get_data(csvfile):
    reader = csv.DictReader(csvfile)
    return zip(*[
        (
            row['page_size'], 
            row['milliseconds_elapsed'],
            # calculate data rate: mebibytes / second
            (
                # convert bytes -> mebibytes
                (int(row['page_size']) / 2 ** 20)
                /
                # convert milliseconds -> seconds
                100/(int(row['milliseconds_elapsed']) / 1000)
            )
        )
        for row in reader
    ])
with open('./results_write.csv') as csvfile:
    x, y, rates = get_data(csvfile)
    
    plt.title(
        'Performance of write_fixed_len_pages ' +
        'with different page_sizes'
    )
    plt.xlabel('Page Size (Bytes)')
    plt.ylabel('Records/Seconds')
    plt.xscale('log')
    plt.plot(x, rates, 'bo')
    
    plt.show()
# In[5]:
get_ipython().run_line_magic('matplotlib', 'inline')
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
def get_data(csvfile):
    reader = csv.DictReader(csvfile)
    return zip(*[
        (
            row['page_size'], 
            row['milliseconds_elapsed'],
            # calculate data rate: mebibytes / second
            (
                # convert bytes -> mebibytes
                (int(row['page_size']) / 2 ** 20)
                /
                # convert milliseconds -> seconds
                100/(int(row['milliseconds_elapsed']) / 1000)
            )
        )
        for row in reader
    ])
with open('./results_read.csv') as csvfile:
    x, y, rates = get_data(csvfile)
    
    plt.title(
        'Performance of read_fixed_len_pages ' +
        'with different page_sizes'
    )
    plt.xlabel('Page Size (Bytes)')
    plt.ylabel('Records/Seconds')
    plt.xscale('log')
    plt.plot(x, rates, 'bo')
    
    plt.show()