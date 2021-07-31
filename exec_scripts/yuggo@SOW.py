#!/usr/bin/env python
# coding: utf-8
# In[1]:
#you have to make sure that you have all of these installed
import cProfile
import re
import math
import numpy as np
import scipy as sp
from scipy import stats
from scipy import optimize as opt
import pandas as pd
import random as rnd
from matplotlib import pyplot as plt
import time
import numpy.random
import warnings
warnings.filterwarnings('ignore')
import multiprocessing as mp
# In[2]:
import chen_utils as ch
import user_simulation_utils as sim
# In[3]:
###Generation of people and their characteristics
np.random.seed(123)
# beta predictors
# assume beta (rate parameter) is determined by avg. transaction size
# avg income and whether public transport was used and loyalty programm membership
# create this feature matrix
Std = 0.02
People = 50
mean_transaction = np.random.normal(np.log(15), Std, People)
mean_transaction = np.exp(mean_transaction)
mean_income = np.random.normal(1800, 100, People)
public_transport = [0] * 5 + [1] * 5
public_transport = np.array(public_transport * 5)
# p predictors
# assume p (SOW) is driven by loyalty card membership and whether discounter is present
# create this feature matrix
# membership in loyalty
loyalty = np.random.binomial(1, 0.6, 50)
discounter = np.array([0, 1] * 25)
preference = np.array(stats.uniform.rvs(0, 1, size=People, random_state = 123))
theta_beta = 1 -0.2*mean_transaction + 0.0005*mean_income + 0.5*public_transport + 0.6*loyalty + np.random.normal(0.01, 0.01, People) 
beta = np.exp(theta_beta) 
theta_p = -0.2 +0.4*loyalty - 0.8*discounter + preference + np.random.normal(0.01, 0.01, People)
p = sim.expit(theta_p)
# In[4]:
covariates = pd.DataFrame({'mean_transaction': mean_transaction, 'mean_income': mean_income, 'public_transport': public_transport, 'loyalty': loyalty, 'discounter': discounter, 'preference': preference, 'true_beta': beta, 'true_p': p})
covariates
# In[16]:
covariates.to_csv('covariates.csv', sep=',', encoding='utf-8',index=False)
# In[5]:
#check distribution of beta and p
plt.hist(beta)
plt.show()
plt.hist(p)
plt.show()
# In[6]:
observations = []
for i in range(len(p)):
    observations.append(sim.simulate_data(share_observed = p[i], rate_input = beta[i], observations_total = 20))
# In[7]:
observations[0:3]
# In[8]:
npinput = np.asarray(observations)
# delete all last purchase bigger than 30
# check mapping and potentially keep user_id --> check
print("2 parameter model")
pool = mp.Pool(processes = None)
t0 = time.time()
results_2par = pool.map(ch.metropolis_solution_trajectory, npinput)
t1 = time.time()
print(t1-t0)
# In[12]:
results_2par[0:2]
# In[13]:
final_results = np.zeros((len(results_2par)*len(results_2par[0]), 2))
final_ids = np.zeros((len(results_2par)*len(results_2par[0]), 1))
for i in range(len(results_2par)):
    for j in range(len(results_2par[i])):
        final_results[i*len(results_2par[i])+j] = [results_2par[i][j][0], results_2par[i][j][1]]
        final_ids[i*len(results_2par[i])+j] = i + 1
# In[14]:
final_results
# In[15]:
df = pd.DataFrame({'user_category_ids': final_ids.ravel(), '2par_first': final_results[:,0].ravel(), '2par_second': final_results[:,1].ravel()})
df
# In[24]:
df.to_csv('metropolis_trajectory.csv', sep=',', encoding='utf-8',index=False)