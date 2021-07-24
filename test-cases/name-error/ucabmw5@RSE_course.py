#!/usr/bin/env python
# coding: utf-8
# In[17]:
import requests
spots=requests.get('http://www.sidc.be/silso/INFO/snmtotcsv.php')
spots.text.split('\n')[0]
# In[3]:
import numpy as np
import requests
# In[4]:
spots=requests.get('http://www.sidc.be/silso/INFO/snmtotcsv.php', stream=True)
# In[5]:
sunspots= np.genfromtxt(spots.raw, delimiter=';')
# In[10]:
sunspots[0][3]
# In[12]:
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt
plt.plot(sunspots[:,2], sunspots[:,3]) # Numpy syntax to access all 
                                       #rows, specified column.
# In[6]:
sunspots= np.genfromtxt(StringIO(spots), delimiter=';', 
                        names=['year','month','date',
                        'mean','deviation','observations','definitive'])
# In[7]:
sunspots
# In[36]:
spots=requests.get('http://www.sidc.be/silso/INFO/snmtotcsv.php')
from io import BytesIO
data = BytesIO(spots.content)
sunspots= np.genfromtxt(data, delimiter=';', 
                        names=['year','month','date',
                        'mean','deviation','observations','definitive'],
                        dtype=[int, int, float, float, float, int, int])
# In[37]:
sunspots
# In[10]:
sunspots['year']
# In[11]:
plt.plot(sunspots['year'],sunspots['mean'])