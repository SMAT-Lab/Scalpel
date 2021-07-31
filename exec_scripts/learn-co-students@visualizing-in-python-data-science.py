#!/usr/bin/env python
# coding: utf-8
# In[1]:
import plotly
plotly.offline.init_notebook_mode(connected=True)
# use offline mode to avoid initial registration
# In[2]:
import plotly
plotly.offline.init_notebook_mode(connected=True)
# we repeat these first lines just to keep the code together  
trace0 = dict(x=[4, 1, 5, 6, 3, 5], y=[8, 11, 8, 13, 6, 4])
# All that, and it doesn't even look good :(
plotly.offline.iplot([trace0])
# In[3]:
trace1 = dict(x=[4, 1, 5, 6, 3, 5],
              y=[8, 11, 8, 13, 6, 4], 
              mode="markers", 
              text=["bob", "suzie", "fred", "edgar", "steven", "natalie"],)
plotly.offline.iplot([trace1])
# much better :)