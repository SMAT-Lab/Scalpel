#!/usr/bin/env python
# coding: utf-8
# In[24]:
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from central_limit_theorem import *
sample_sizes = [1, 2, 10, 100, 1000, 10000]
number_of_samples = 10000
for i, sample_size in enumerate(sample_sizes):
    means = clt(sample_size=sample_size, number_of_samples=number_of_samples)
#     print(means)
    plt.subplot(len(sample_sizes), 1, i+1)
    plt.hist(means, bins='auto')
# In[35]:
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from central_limit_theorem import *
sample_sizes = [1000]
number_of_samples = 10000
for i, sample_size in enumerate(sample_sizes):
    means = clt(sample_size=sample_size, number_of_samples=number_of_samples)
#     print(means)
    plt.subplot(len(sample_sizes), 1, i+1)
    plt.hist(means, bins='auto')