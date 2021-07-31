#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.mlab as mlab
# In[4]:
N     = 10000;
mu    = 1;
sigma = 1;
np.random.seed(2018)
# In[10]:
NormalDraws = mu + sigma*np.random.normal(0,1,(N,1));
num_bins = 100 #round(N/100);
n, bins, patches = plot.hist(NormalDraws,num_bins,normed=1);
y = mlab.normpdf(bins, mu, sigma);
plot.plot(bins, y,'r--');
# In[74]:
mu = 0.0;
sigma = 1;
np.random.seed(2018)
N_vec = np.array(np.int_(np.linspace(10,10000,100)));
num   = N_vec.size;
mean_vec = np.zeros((num,1));
std_vec  = np.zeros((num,1));
for i in range(num):
    draws = mu + sigma*np.random.normal(0,1,(N_vec[i],1));
    mean_vec[i] = np.mean(draws);
    std_vec[i]  = np.sqrt(np.var(draws));
plot.figure()    
true_mu = mu + np.zeros((num,1))
plot.plot(N_vec,true_mu)      
plot.plot(N_vec,mean_vec);
plot.title("Mean, $\mu$");
plot.figure()
true_sigma = sigma + np.zeros((num,1))
plot.plot(N_vec,true_sigma)      
plot.plot(N_vec,std_vec);
plot.title("Std, $\sigma$");  