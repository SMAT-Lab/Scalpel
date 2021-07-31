#!/usr/bin/env python
# coding: utf-8
# In[1]:
from Bplate import *
from sage2d import *
components =1
c = csi_matrix()
file_corr='./raw_files/log_file_corr.dat'
file_target='./raw_files/log_file_target.dat'
csi = c.final_matrix(file_corr, file_target)
# In[2]:
s = sage2d()
[Tx,Rx,Subcarrier,length]=csi.shape
dod=np.zeros((length))
doa=np.zeros((length))
for i in range(0,length):
    [beta, f1, f2, CostFunction1, CostFunction2] = s.sage(csi[:, :, 0,i], components)
    if f1.size > 0:
        dod[i]=np.squeeze((np.arcsin(np.abs(f1) / 0.5)*180/np.pi))
        doa[i]=np.squeeze((np.arcsin(np.abs(f2) / 0.5)*180/np.pi))
# In[3]:
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
f, axarr = plt.subplots(1, 2 ,figsize=(20,10))
plot=axarr[0].plot(np.transpose(dod) ,'b');
plot=axarr[1].plot(np.transpose(doa),'g');
l=plt.show;