#!/usr/bin/env python
# coding: utf-8
# In[1]:
# %load_ext autoreload
# %autoreload 2
# In[8]:
from notebook_autorun import Autorun
cells = '3,-1'
Autorun(cells=cells, metadata=False, comment=False, focus=None, verbose=True).add_js()
# in nbviewer.org the Javascript object (code) and Markdown object (status msg) are displayed
# as there is no security mechanism disabling their execution - as opposed to the real notebook
# So you should see the following, instead of the actual status message:
#
#<IPython.core.display.Javascript object>
#
#<IPython.core.display.Markdown object>
# In[1]:
# manually executed after previous cell failure and indication
from notebook_autorun import Autorun; Autorun.info()