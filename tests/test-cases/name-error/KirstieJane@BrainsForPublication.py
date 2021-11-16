#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
# In[2]:
stats_file = '../test_data/ALL_N95_Mean_cope2_thresh_zstat1.nii.gz'
view =  'ortho'
colormap = 'RdBu_r'
threshold = '2.3'
black_bg
# In[13]:
get_ipython().run_line_magic('run', '../scripts/mni_glass_brain.py --cbar --display_mode $view --cmap $colormap --thr_abs $threshold $stats_file')
# In[14]:
from IPython.display import Image, display
from glob import glob as gg
outputs = gg('../test_data/*ortho.png')
for o in outputs:
    a = Image(filename=o)
    display(a)
# In[9]:
get_ipython().run_line_magic('pinfo2', 'plotting.plot_glass_brain')