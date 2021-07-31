#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
get_ipython().run_line_magic('matplotlib', 'inline')
points = np.array([[1.5, 1.], [3.5, 1.], [5., 2.], [2.5, 3.], [3.5, 1.], 
                   [4., 4.], [5.5, 3.5], [6., 5.5], [7.5, 4], [1.6, 6.]])
fig = plt.figure()
ax = fig.add_subplot('111')
ax.plot(points[:, 0], points[:, 1], 'o', color='k')
ax.set_xlim([-1, 9])
ax.set_ylim([-1, 9])
# In[2]:
from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(points)
fig = plt.figure()
ax = fig.add_subplot('111')
ax.plot(points[:, 0], points[:, 1], 'o', color='k')
ax.set_xlim([-1, 9])
ax.set_ylim([-1, 9])
voronoi_plot_2d(vor, ax)
# In[3]:
from scipy.spatial import Delaunay
tri = Delaunay(points)
fig = plt.figure()
ax = fig.add_subplot('111')
ax.plot(points[:, 0], points[:, 1], 'o', color='k')
ax.set_xlim([-1, 9])
ax.set_ylim([-1, 9])
ax.triplot(points[:,0], points[:,1], tri.simplices.copy(), color='blue')
# In[4]:
fig = plt.figure()
ax = fig.add_subplot('111')
ax.plot(points[:, 0], points[:, 1], 'o', color='k')
ax.set_xlim([-1, 9])
ax.set_ylim([-1, 9])
voronoi_plot_2d(vor, ax)
ax.triplot(points[:,0], points[:,1], tri.simplices.copy(), color='blue')