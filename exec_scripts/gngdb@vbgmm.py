#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().system('wget http://www.stat.cmu.edu/~larry/all-of-statistics/=data/faithful.dat')
# In[2]:
get_ipython().system('head -n 30 faithful.dat')
# In[3]:
get_ipython().system('tail -n+26 faithful.dat > faithful.csv')
# In[12]:
import numpy as np
from scipy.special import psi as digamma
# In[5]:
data = np.loadtxt("faithful.csv",skiprows=1)
# In[6]:
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# In[7]:
plt.scatter(data[:,1],data[:,2])
# In[13]:
# initialise prior parameters
k = 2
alpha_0 = 1.
m_0 = np.zeros(k)
# just making the Wishart covariance diagonal as well
v_0 = 1.
W_0 = np.eye(k)*v_0
beta_0 = 1.
D = 2
# In[14]:
# initialise variational update functions
##########
# M step #
##########
def _lnrho_nk(E_lnpi_k, E_lnLambda_k, D, E_mu_k_Lambda_k):
    return E_lnpi_k + 0.5*E_lnLambda_k - (D/2.)*np.log(2.0*np.pi) - 0.5*E_mu_k_Lambda_k
def _r_k(rho_k):
    return rho_k/np.sum(rho_k, axis=1)
def _N_k(r_k):
    return np.sum(r_k)
def _x_bar_k(N_k, r_k, X):
    return (1./N_k)*np.dot(X,r_k)
def _S_k(N_k, r_k, x_bar_k):
    return (1./N_k)*np.dot(np.dot((X-x_bar_k.T).T, X-x_bar_k.T),r_k)
def _alpha(alpha_0, N):
    return alpha_0 + N
def _beta(beta_0, N):
    return beta_0 + N
def _m_k(beta_0, beta_k, m_0, N_k, x_bar_k):
    return (1./beta_k)*(beta_0*m_0 + N_k*x_bar_k)
def _invW_k(W_0, N_k, S_k, beta_0, x_bar_k, m_0):
    return np.linalg.inv(W_0) + N_k*S_k +            ((beta_0*N_k)/(beta_0 + N_k))*np.dot(x_bar_k-m_0, (x_bar_k - m_0).T)
def _v_k(v_0, N_k):
    return v_0 + N_k
##########
# E Step #
########## 
def _alpha_hat(alpha):
    return np.sum(alpha)
def _E_lnpi_k(alpha_k, alpha_hat):
    return digamma(alpha_k) - digamma(alpha_hat)
def _E_lnLambda_k(W_k, v_k, D):
    D_its = np.zeros(D)
    for i in range(D):
        D_its[i] = digamma((v_k+1-i)/(2.)) + D*np.log(2) + np.log(np.linalg.det(W_k))
    return np.sum(D_its)
        
def _E_mu_k_Lambda_k(X, beta_k, v_k, m_k, W_k):
    return D*beta_k**-1 + v_k*np.dot(np.dot((X-m_k.T), W_k), (X-m_k.T).T)
# Confused yet?
# In[20]:
# we need to be able to visualise the distribution we've learnt to have
# any idea if it's working
def normal_density(x, mu, Sigma):
    return (1./np.sqrt(2.*np.pi*np.linalg.det(Sigma)))            *np.exp(-0.5*np.dot(np.dot((x-mu).T, np.linalg.inv(Sigma)),(x-mu)))
from scipy.special import multigammaln
def wishart_density(X, n, V):
    p = X.shape[0]
    assert X.shape[1] == p
    normalising = (2.0**(n*p/2.0))*np.power(np.linalg.det(V), n/2.)
    return (np.power(np.det(X), (n-p-1)/2)*            np.exp(-0.5*np.trace(np.dot(np.linalg.inv(V), X))))/normalising
    
def get_p_mu_k(m_0, beta_0, Lambda_k):
    return lambda mu: normal_density(mu, m_0, np.linalg.inv(beta_0*Lambda_k))
# PENDING: Dirichlet and complete density of mixture...