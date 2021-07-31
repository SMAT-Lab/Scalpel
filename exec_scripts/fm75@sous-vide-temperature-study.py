#!/usr/bin/env python
# coding: utf-8
# In[1]:
import pandas as pd
# In[2]:
from bqplot import *
# In[3]:
inputfile = 'TBone-1-inch.txt'
# In[4]:
foodtype, thickness, measure = inputfile.split ('-')
all = pd.read_csv (inputfile)
x_sc = LinearScale()
y_sc = LinearScale()
ax_x = Axis(label='Elapsed Time', scale=x_sc, grid_lines='solid')
ax_y = Axis(label='Temperature °C',  scale=y_sc, orientation='vertical', grid_lines='solid')
line = Lines(x=all['ElapsedTime'], y=[all[foodtype], all['Bath']], scales={'x': x_sc, 'y': y_sc})
fig = Figure(axes=[ax_x, ax_y], marks=[line], title=foodtype + ' Temperature')
fig
# In[5]:
inputfile = 'Swordfish-1-inch.txt'
# In[6]:
foodtype, thickness, measure = inputfile.split ('-')
all = pd.read_csv (inputfile)
x_sc = LinearScale()
y_sc = LinearScale()
ax_x = Axis(label='Elapsed Time', scale=x_sc, grid_lines='solid')
ax_y = Axis(label='Temperature °C',  scale=y_sc, orientation='vertical', grid_lines='solid')
line = Lines(x=all['ElapsedTime'], y=[all[foodtype], all['Bath']], scales={'x': x_sc, 'y': y_sc})
fig = Figure(axes=[ax_x, ax_y], marks=[line], title=foodtype + ' Temperature')
fig