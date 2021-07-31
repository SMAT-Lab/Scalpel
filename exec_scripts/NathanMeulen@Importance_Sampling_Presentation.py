#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
get_ipython().run_line_magic('matplotlib', 'inline')
# In[2]:
fig, ax = plt.subplots(1,2, figsize=(15,5))
x = np.random.random(1000000)
x1 = np.random.randn(1000000)
#*******Plotting*******
ax[0].hist(x, bins=50, ec='black', color='yellow', normed=True)
ax[0].set_title('Uniform distribution (Numpy.random.random)', fontsize=15)
ax[1].hist(x1, bins=50, ec='black', color='yellow', normed=True)
ax[1].set_title('Normal distribution (Numpy.random.randn)', fontsize=15);
# In[3]:
def fn(x):
    return 10*np.exp(-5*(x**4))
def normal_distribution(x, mu, sigma):
    return (1/np.sqrt(2*np.pi*sigma*sigma))*np.exp(-((x-mu)**2)/(2*sigma*sigma))
def example1():
    xvals = np.linspace(-4,4,10000)
    fig,ax = plt.subplots(1,2, figsize=(15,5))
    ax[0].plot(xvals, fn(xvals))
    ax[0].set_title('$f(x)$: The function we want the expectation value for', fontsize=15)
    ax[0].set_ylim(ymin=0)
    ax[0].set_ylabel('f(x)', fontsize=20)
    ax[0].set_xlabel('x', fontsize=20)
    ax[0].grid('on')
    ax[1].plot(xvals, normal_distribution(xvals,0,1));
    ax[1].set_xlabel('x', fontsize=20)
    ax[1].set_ylabel('$p(x)$', fontsize=20)
    ax[1].set_ylim(ymin=0)
    ax[1].set_title('p(x): Sampling from a normal distribution ($\sigma=1$ and $\mu=0$)', fontsize=15)
    ax[1].grid('on')
    plt.tight_layout()
    return
example1()
# In[4]:
# get 10000000 from the standard normal distribution
x = np.random.randn(10000000)
# find fn(x) for each x value
fx = fn(x)
# calculate the approximate expectation value
# by taking the average of fn(x)
fx_avg = np.average(fn(x))
print("Expectation value:", fx_avg)
# In[5]:
def fn_shifted(x):
    return 10*np.exp(-5*((x-3)**4))
def example2():
    # Use standard Monte Carlo to find the 
    # approximate expectation value 500 times
    f_vals = []
    count = 0
    while(count<500):
        # get a sample of 1000 random values from p(x)
        x = np.random.randn(1000)
        # find the average value of f(x) 
        fx = np.average(fn_shifted(x))
        # store the average value of f(x) 
        # in the array f_vals
        f_vals.append(fx)
        count += 1
    # plot the results
    plt.figure(figsize=(10,5))
    plt.grid('on')
    plt.plot(f_vals, linewidth='0.5')
    plt.plot(np.arange(500), np.ones(500)*0.089399, '--', label='Calculated expected value = 0.089399')
    plt.ylim(0.02,0.18)
    plt.title('The Monte-Carlo approximation of $E(f(x))$ over 500 trials', fontsize=20)
    plt.xlabel('trial', fontsize=20)
    plt.ylabel('approximate $E(f(x))$', fontsize=20)
    plt.legend(loc='best', fontsize=15)
    
    # print the average and standard deviation
    print('Average expected value over 500 trials',np.average(f_vals))
    print('Standard deviation in the average expected value', np.std(f_vals))
    
example2()
# In[6]:
def example3(mu_p=0, sigma_p=1, mu_q=3, sigma_q=1):
    xvals = np.linspace(-4,7,10000)
    fig,ax = plt.subplots(1,3, figsize=(25,5))
    ax[0].plot(xvals, fn_shifted(xvals))
    ax[0].set_title('$f(x)$: The function we want the expectation value for', fontsize=20)
    ax[0].plot(np.ones(10)*3, np.linspace(-1,12,10), '--')
    ax[0].set_ylim(0,11)
    ax[0].set_ylabel('f(x)', fontsize=20)
    ax[0].set_xlabel('x', fontsize=20)
    ax[0].grid('on')
    ax[1].plot(xvals, normal_distribution(xvals,mu_p,sigma_p));
    ax[1].set_xlabel('x', fontsize=20)
    ax[1].set_ylabel('$p(x)$', fontsize=20)
    ax[1].plot(np.ones(10)*3, np.linspace(-1,1,10), '--')
    ax[1].set_ylim(0,0.2)
    ax[1].set_title('p(x): Sampling from a normal distribution ($\sigma=1$ and $\mu=0$)', fontsize=20)
    ax[1].grid('on')
    ax[2].plot(xvals, normal_distribution(xvals,mu_q,sigma_q));
    ax[2].set_xlabel('x', fontsize=20)
    ax[2].set_ylabel('$q(x)$', fontsize=20)
    ax[2].plot(np.ones(10)*3, np.linspace(-1,1,10), '--')
    ax[2].set_ylim(0,0.2)
    ax[2].set_title('q(x): Alternate normal distribution ($\sigma=1$ and $\mu=3$)', fontsize=20)
    ax[2].grid('on')
    plt.tight_layout()
    return
example3()
# In[13]:
def importance_sampling(fn=fn_shifted, count=500, mu_p=0, sigma_p=1, mu_q=3, sigma_q=1):
    f_vals = []
    # Use importance sampling and Monte Carlo to find the 
    # approximate expectation value 500 times
    for i in range(count):
        # q(x)
        randq = sigma_q*np.random.randn(1000)+mu_q
        # find the average value of f(x) 
        importance_sampling = fn(randq)*normal_distribution(randq,mu_p,sigma_p)/normal_distribution(randq,mu_q,sigma_q)
        fx = np.average(importance_sampling)
        f_vals.append(fx)
    print('Average expected value over', count, 'trials', np.average(f_vals))
    print('Standard deviation in the average expected value', np.std(f_vals))
    # Computing the continuous integral using quad rather than Monte Carlo integration for comparison
    calculated = integrate.quad(lambda x: fn(x)*normal_distribution(x, mu_p, sigma_p), -np.inf, np.inf)[0]
    plt.figure(figsize=(10,5))
    plt.grid('on')
    plt.plot(f_vals, linewidth='0.5')
    plt.plot(np.arange(count), np.ones(count)*calculated, '--', label='Calculated expected value = {:0.5f}'.format(calculated))
    plt.title('Using importance sampling $E(f(x))$ over ' + str(count) + ' trials', fontsize=20)
    plt.xlabel('trial', fontsize=20)
    plt.ylabel('approximate $E(f(x))$', fontsize=20)
    plt.legend(loc='best', fontsize=15)
    plt.ylim(0.02,0.18); # Comment out this line if you change the parameters
    return
importance_sampling()