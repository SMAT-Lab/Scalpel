#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
# In[2]:
import matplotlib.pyplot as plt 
import numpy as np 
# from __future__ import division  (if you're using Python 2.7+, to make float division the default)
# In[3]:
Ts = 1 # sampling interval is 1 second
t_start = -10 # First sampled timepoint is at -10s (let's say that's 10s before the concert starts)
t_stop = 17 # Last sampled timepoint is at 17s (let's say this is 17s after the concert starts)
ns = (t_stop - t_start) / Ts + 1 # compute number of sampled timepoints
print(ns)
# In[4]:
fs = 1/Ts # sampling frequency
ns = (t_stop - t_start) * fs + 1
print(ns)
# In[5]:
fs = 100 # define the sampling rate, f_s = 100 Hz
t_start = 0 # We start sampling at t = 0s
t_stop =  10 # We stop sampling at t = 10s
ns = (t_stop - t_start) * fs + 1
x = np.linspace(t_start, t_stop, ns)
# In[6]:
#help(np.arange) #Uncomment this to get documentation on np.arange
fs = 100 # define the sampling rate, f_s = 100 Hz
t_start = 0 # We start sampling at t = 0s
t_stop =  10 # We stop sampling at t = 10s
ns = (t_stop - t_start) * fs + 1
x_arange = np.arange(t_start, t_stop + 1/fs, 1/fs) # Define vector of sampled time points
# In[7]:
f1 = 440 # frequency of y_1(t)
f2 = 220 # frequency of y_2(t)
y1 = np.sin(2*np.pi*f1*x)
y2 = np.sin(2*np.pi*f2*x)
# In[8]:
plt.plot(x , y1, "-g", label="y1") # plot (x,y1) as a green line
plt.plot(x , y2, "-b", label="y2") # plot (x,y2) as a blue line
plt.legend(loc="upper right") 
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (dB)')
# In[9]:
plt.xlim(0,0.3)
plt.plot(x , y1, "-g", label="y1") # plot (x,y1) as a green line
plt.plot(x , y2, "-b", label="y2") # plot (x,y2) as a blue line
#plt.stem(x,y1, 'r', )
plt.legend(loc="upper right") 
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (dB)')
#plt.plot(x,y1)
# In[10]:
plt.xlim(0,0.3)
plt.plot(x , y1, "-g", label="y1") # plot (x,y1) as a green line
plt.plot(x , y2, "-b", label="y2") # plot (x,y2) as a blue line
#plt.stem(x,y1, 'r', )
plt.legend(loc="upper right") 
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (dB)')
#plt.plot(x,y1)
# In[11]:
plt.xlim(0,0.3)
plt.stem(x,y1, 'g', label='y1')
plt.stem(x,y2, 'b', label='y2')
plt.legend(loc="upper right") 
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (dB)')
# In[12]:
from IPython.display import Audio
# In[18]:
fs = 44100 # define the sampling rate, f_s = 144100 Hz
t_start = 0 # We start sampling at t = 0s
t_stop =  3 # We stop sampling at t = 3s
ns = (t_stop - t_start) * fs + 1
x = np.linspace(t_start, t_stop, ns)
f1 = 440 # frequency of y_1(t)
f2 = 220 # frequency of y_2(t)
y1 = np.sin(2*np.pi*f1*x)
y2 = np.sin(2*np.pi*f2*x)
# In[20]:
Audio(data=y1, rate=fs)
# In[22]:
Audio(data=y2, rate=fs)
# In[16]:
Audio(url="http://www.w3schools.com/html/horse.ogg")
# In[17]:
Audio('crow.wav')