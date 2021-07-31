#!/usr/bin/env python
# coding: utf-8
# In[16]:
import geopandas as gpd
get_ipython().run_line_magic('pylab', 'inline')
pylab.rcParams['figure.figsize'] = (20.0, 20.0)
import shapely
# In[17]:
villages_shap = gpd.read_file('kbike0324.shp')
# In[18]:
villages_shap.head()
villages_shap
# In[19]:
broad = villages_shap[villages_shap['system'] == '阿公店自行車道']
loveroad = villages_shap[villages_shap['system'] == '博愛世運大道']
# In[20]:
len(broad)
# In[24]:
ax = broad.plot(linewidth=3, color='Orange')
loveroad.plot(linewidth=3, ax=ax, color='Blue')