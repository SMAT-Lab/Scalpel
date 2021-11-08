#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np 
import nglview as nv
from falass import readwrite, job, sld, reflect, compare
# In[2]:
files = readwrite.Files(datfile='example/example.dat')
# In[3]:
# In[4]:
files.read_dat()
# In[5]:
expdata = files.plot_dat(rq4=False)
expdata.show()
# In[6]:
mono_init = pt.load('example/monolayer.pdb')
view = nv.show_pytraj(mono_init)
view
# In[7]:
files.pdbfile = 'example/example.pdb'
files.flip = True
files.read_pdb()
# In[8]:
# In[9]:
files.lgtfile = 'example/example.lgt'
files.read_lgt()
# In[10]:
layer_thickness = 1.
cut_off = 5.
job = job.Job(files, layer_thickness, cut_off)
job.set_lgts()
# In[11]:
sld = sld.SLD(job)
sld.get_sld_profile()
sld.average_sld_profile()
sld.plot_sld_profile()
# In[12]:
reflect = reflect.Reflect(sld.sld_profile, files.expdata)
reflect.calc_ref()
reflect.average_ref() 
reflect.plot_ref(rq4=False)
# In[13]:
compare = compare.Compare(files.expdata, reflect.averagereflect, 1e-1, 1e-6)
compare.fit()
compare.return_fitted()
compare.plot_compare()