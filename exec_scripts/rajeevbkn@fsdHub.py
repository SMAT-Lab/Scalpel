#!/usr/bin/env python
# coding: utf-8
# In[1]:
# The programme shows functionality of matplotlib in a simple x-y graph.
from matplotlib import pyplot as plt
import numpy as np
plt.plot([1, 2, 3, 4], [1, 6, 9, 16])
plt.title('Velocity-Time Graph')
plt.xlabel('Time, in sec')
plt.ylabel('Velocity, in m/s')
plt.show()