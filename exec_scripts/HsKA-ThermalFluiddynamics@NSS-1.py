#!/usr/bin/env python
# coding: utf-8
# In[1]:
from IPython.core.display import HTML
def css_styling():
    styles = open('TFDStyle.css', 'r').read()
    return HTML(styles)
css_styling()