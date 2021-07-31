#!/usr/bin/env python
# coding: utf-8
# In[1]:
import scipy as sc
from scipy.stats import bernoulli
from scipy.stats import binom
from scipy.stats import norm
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (10, 6)
# In[2]:
n = 1000;
coin_flips = bernoulli.rvs(p=0.5, size=n)
print(coin_flips)
# In[3]:
print(sum(coin_flips))
print(sum(coin_flips)/n)
# In[4]:
n = 1000000
coin_flips = bernoulli.rvs(p=0.5, size=n)
print(sum(coin_flips)/n)
# In[5]:
p = 0.5
n = 10
bin_vars = binom.rvs(n=n,p=p,size=1000000)
print(bin_vars[:100])
# In[6]:
bins=sc.arange(12)-.5
plt.hist(bin_vars, bins=bins,normed=True)
plt.title("A histogram of binomial random variables")
plt.xlim([-.5,10.5])
plt.show()
# In[7]:
f = lambda k: binom.pmf(k, n=n,p=p)
x = sc.arange(n+1);
plt.plot(x, f(x),'*-')
plt.title("The probability mass function for a Binomial random variable")
plt.xlim([0,n])
plt.show()
# In[8]:
mu = 0 # mean
sigma = 1 # standard deviation 
x = sc.arange(mu-4*sigma,mu+4*sigma,0.001);
pdf = norm.pdf(x,loc=mu, scale=sigma)
# Here, I could have also written
# pdf = 1/(sigma * sc.sqrt(2 * sc.pi)) * sc.exp( - (x - mu)**2 / (2 * sigma**2)) 
plt.plot(x, pdf, linewidth=2, color='k')
plt.show()
# In[9]:
plt.plot(x, pdf, linewidth=2, color='k')
x2 = sc.arange(mu-sigma,mu+sigma,0.001)
plt.fill_between(x2, y1= norm.pdf(x2,loc=mu, scale=sigma), facecolor='red', alpha=0.5)
plt.show()
# In[10]:
norm.cdf(mu+sigma, loc=mu, scale=sigma) - norm.cdf(mu-sigma, loc=mu, scale=sigma) 
# In[11]:
norm_vars = norm.rvs(loc=mu,scale=sigma,size=1000000)
print(norm_vars[:100])
plt.hist(norm_vars, bins=100,normed=True)
plt.plot(x, pdf, linewidth=2, color='k')
plt.title("A histogram of normal random variables")
plt.show()
# In[12]:
n = 1000
p = 0.5
bin_vars = binom.rvs(n=n,p=p,size=10000)
plt.hist(bin_vars, bins='auto',normed=True)
mu = n*p 
sigma = sc.sqrt(n*p*(1-p))
x = sc.arange(mu-4*sigma,mu+4*sigma,0.1);
pdf = norm.pdf(x, loc=mu, scale=sigma)
# Here, I could also write 
# pdf = 1/(sigma * sc.sqrt(2 * sc.pi)) * sc.exp( - (x - mu)**2 / (2 * sigma**2) ) 
plt.plot(x, pdf, linewidth=2, color='k')
plt.title("A comparison between the histogram of binomial random \n variables and the normal distribution predicted by the CLT")
plt.show()
# In[13]:
n = 1000
p = 0.5
mu = n*p
sigma = sc.sqrt(n*p*(1-p))
print(norm.cdf(545, loc=mu, scale=sigma))
# a plot illustrating the integral 
x = sc.arange(mu-4*sigma,mu+4*sigma,0.001);
plt.plot(x, norm.pdf(x, loc=mu, scale=sigma), linewidth=2, color='k')
x2 = sc.arange(mu-4*sigma,545,0.001)
plt.fill_between(x2, y1= norm.pdf(x2,loc=mu, scale=sigma), facecolor='red', alpha=0.5)
plt.xlim([mu-4*sigma,mu+4*sigma])
plt.show()
# In[14]:
val_integral = norm.cdf(545, loc=mu, scale=sigma) - norm.cdf(455, loc=mu, scale=sigma)
print(val_integral)
print(1-val_integral)
# In[15]:
mu = 15
sigma = sc.sqrt(5.72**2/137)
print(2*norm.cdf(2.42, loc=mu, scale=sigma))