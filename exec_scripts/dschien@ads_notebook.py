#!/usr/bin/env python
# coding: utf-8
# In[4]:
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets
from IPython.display import display
# In[6]:
def on_button_clicked(ev):
    from IPython import display
    display.clear_output(wait=True)
    if plotW.value == '1':
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2*np.pi*t)
        plt.plot(t, s)
    else:
        plt.plot([1,2,3,4])        
        
plotW = widgets.Dropdown(options=['1','2'],description='Scenario')
button = widgets.Button(description="Plot")
button.on_click(on_button_clicked)
container = widgets.Box(children=[plotW , button])
display(container)