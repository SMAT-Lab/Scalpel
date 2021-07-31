#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from matplotlib import cm
plt.rcParams['font.size'] = 14
plt.rcParams['axes.spines.right'] = False
plt.rcParams['ytick.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['xtick.top'] = False
# Get n grayscale colors
def getGrayColors(n):
    colors = [];
    for i in range(1, n+1):
        colors.append(i/(n+1.)*np.ones(3))
    return colors
# In[2]:
# The soft-rectifying function (f), also known as the inverse of the link function for generalized linear models
def invLinkFun(X, w):
    z = np.dot(X, w)
    mu = np.zeros(z.shape)
    mu[z<0] = np.exp(z[z<0])
    mu[z>=0] = z[z>=0] + 1
    return mu
# Parameters
n = 200;           # Number of data points
wTrue = [-1, 0.5]  # w0 and w1 for the simulated data
# Generate example data
x = np.random.rand(n)*30 - 15
x = np.sort(x)
X = np.vstack([-np.ones(n), x]).T
mu = invLinkFun(X, wTrue)
y = np.random.poisson(mu)
# Callback plotting function for interactive plots
def plot_fun(x, y, w0, w1):
    fig = plt.figure(figsize=(7.5, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y, 'k.', label='data')
    wTmp = np.array([w0, w1])
    muTmp = invLinkFun(X, wTmp)
    ax.plot(x, muTmp, '-', color=0.5*np.ones(3))
    ax.set_ylabel('Spike count')
    ax.set_xlabel('x')
    ax.set_xticks([-10, 0, 10]);
    ax.set_ylim([-1, 11]);
interact(plot_fun, x=fixed(x), y=fixed(y), w0=(-5., 5.), w1=(-5., 5.));
# In[8]:
# Poisson regression, log-likelihood
logLikFun = lambda X, w, y: np.sum(y*np.log(invLinkFun(X, w))-invLinkFun(X, w))
# In[9]:
# Example parameters
w0Ex = np.array([wTrue[0]-4, wTrue[0], wTrue[0]+4])
w0Vals = np.linspace(wTrue[0]-5, wTrue[0]+5, 101)
# Log-likelihood function over the whole interval
ll = np.empty_like(w0Vals)
for i, w0 in enumerate(w0Vals):
    wTmp = np.array([w0, wTrue[1]])
    ll[i] = logLikFun(X, wTmp, y)
# Log-likelihood values for our example parameters
llEx = np.empty_like(w0Ex)
for i, w0 in enumerate(w0Ex):
    wTmp = np.array([w0, wTrue[1]])
    llEx[i] = logLikFun(X, wTmp, y)
# Plotting
grayColors = getGrayColors(3)
fig = plt.figure(figsize=(15, 5))
# Log-likelihood
ax = fig.add_subplot(1, 2, 1)
ax.plot(w0Vals, ll, 'k-')
for i in range(w0Ex.size):
    ax.plot(w0Ex[i], llEx[i], 'o', ms=10, color=grayColors[i])
ax.set_xlabel('$w_0$')
ax.set_ylabel('Log-likelihood')
# Data and example response function mappings
ax = fig.add_subplot(1, 2, 2)
ax.plot(x, y, 'k.', label='data')
for i in range(w0Ex.size):
    wTmp = np.array([w0Ex[i], wTrue[1]])
    pTmp = invLinkFun(X, wTmp)
    ax.plot(x, pTmp, '-', color=grayColors[i])
ax.set_ylabel('Spike count')
ax.set_xlabel('x')
ax.set_xticks([-10, 0, 10]);
# In[11]:
# Example parameters
wEx = np.array([[wTrue[0]-0.9, wTrue[0], wTrue[0]+0.9], [wTrue[1]+0.3, wTrue[1], wTrue[1]-0.3]])
# Get w0 and w1 combinations over a grid
nGrid = 51
W0, W1 = np.meshgrid(np.linspace(wTrue[0]-1, wTrue[0]+1, nGrid), np.linspace(wTrue[1]-0.5, wTrue[1]+0.5, nGrid))
# Get the log-likelihood for each parameter combination
llVals = np.zeros([nGrid, nGrid])
for i in range(nGrid):
    for j in range(nGrid):
        wTmp = np.array([W0[i, j], W1[i, j]])
        llVals[i, j] = logLikFun(X, wTmp, y)
# Plotting
grayColors = getGrayColors(3)
fig = plt.figure(figsize=(15, 5))
# Log-lieklihood and example parameters
ax = plt.subplot(1, 2, 1)
contourHandle = ax.contourf(W0, W1, llVals, 50, cmap=cm.coolwarm)
for i in range(wEx.shape[1]):
    ax.plot(wEx[0, i], wEx[1, i], 'o', ms=10, color=grayColors[i])
ax.set_xlabel('$w_0$')
ax.set_ylabel('$w_1$');
cBarHandle = plt.colorbar(contourHandle)
cBarHandle.set_label('Log-likelihood')
# Data and example response function mappings
ax = fig.add_subplot(1, 2, 2)
ax.plot(x, y, 'k.', label='data')
for i in range(wEx.shape[1]):
    wTmp = wEx[:, i]
    pTmp = invLinkFun(X, wTmp)
    ax.plot(x, pTmp, '-', color=grayColors[i])
ax.set_ylabel('Spike count')
ax.set_xlabel('x')
ax.set_xticks([-10, 0, 10]);
# In[13]:
# Poisson regression, negative log-likelihood
negLogLikFun = lambda X, w, y: np.sum(invLinkFun(X, w) - y*np.log(invLinkFun(X, w)))
# In[14]:
# Poisson regression, gradient of the negative log-likelihood
def negLogLikDerFun(X, w, y):
    z = np.dot(X, w)
    der = np.dot(np.exp(z[z<0])-y[z<0], X[z<0, :])
    der += np.dot(1-y[z>=0]/(z[z>=0]+1), X[z>=0, :])
    return der
# In[15]:
# Use a lower resolution for gradient evaluations
nGrid = 21
W0q, W1q = np.meshgrid(np.linspace(wTrue[0]-1, wTrue[0]+1, nGrid), np.linspace(wTrue[1]-0.5, wTrue[1]+0.5, nGrid))
# Get the gradient for each combination
nllVals = np.zeros([nGrid, nGrid])
W0der = np.zeros([nGrid, nGrid])
W1der = np.zeros([nGrid, nGrid])
for i in range(nGrid):
    for j in range(nGrid):
        wTmp = np.array([W0q[i, j], W1q[i, j]])
        derTmp =  negLogLikDerFun(X, wTmp, y)
        W0der[i, j] = derTmp[0]
        W1der[i, j] = derTmp[1]
# Normalize to unit length
W0derNorm = W0der / np.sqrt(W0der**2. + W1der**2.)
W1derNorm = W1der / np.sqrt(W0der**2. + W1der**2.)
        
# Plotting
grayColors = getGrayColors(3)
fig = plt.figure(figsize=(25, 7))
ax = plt.subplot(1, 1, 1)
ax.set_aspect('equal')
# Negative log-likelihood
contourHandle = ax.contourf(W0, W1, -llVals, 50, cmap=cm.coolwarm)
# Gradient
ax.quiver(W0q, W1q, W0derNorm, W1derNorm, angles='xy', scale_units='xy', scale=30, width=2e-3)
# Axes settings
ax.set_xlabel('$w_0$')
ax.set_ylabel('$w_1$');
cBarHandle = plt.colorbar(contourHandle)
cBarHandle.set_label('negative log-likelihood')
# In[16]:
# Gradient descent parameters
eta = 2e-4
nIterations = 25
wInit = np.array([-1.8, 0.85])
wUpdates = np.zeros([nIterations, 2])
wUpdates[0, :] = wInit
nllVals = np.zeros(nIterations)
nllVals[0] = negLogLikFun(X, wUpdates[0, :], y)
   
# Gradient descent loop
for i in range(1, nIterations):
    wUpdates[i, :] = wUpdates[i-1, :] - eta*negLogLikDerFun(X, wUpdates[i-1, :], y)
    nllVals[i] = negLogLikFun(X, wUpdates[i, :], y)
    
# Plotting
grayColors = getGrayColors(3)
fig = plt.figure(figsize=(25, 7))
ax = plt.subplot(1, 1, 1)
ax.set_aspect('equal')
# Negative log-likelihood
contourHandle = ax.contourf(W0, W1, -llVals, 50, cmap=cm.coolwarm)
# Gradient
ax.quiver(W0q, W1q, W0derNorm, W1derNorm, angles='xy', scale_units='xy', scale=30, width=2e-3)
# Gradient descent progress
ax.plot(wUpdates[:, 0], wUpdates[:, 1], '-o', ms=6, color='white', lw=3)
# Axes settings
ax.set_xlabel('$w_0$')
ax.set_ylabel('$w_1$');
cBarHandle = plt.colorbar(contourHandle)
cBarHandle.set_label('negative log-likelihood')
# In[17]:
w0Init = w0Vals.min()
nllInit = negLogLikFun(X, np.array([w0Init, wTrue[1]]), y)
w0InitDer = negLogLikDerFun(X, np.array([w0Init, wTrue[1]]), y)[0]
offset = nllInit - w0Init*w0InitDer;
# Calculate real and expected decreases
realNllDecrease =  -ll - nllInit
expectedNllDecrease = offset  + w0InitDer*w0Vals - nllInit
# Plotting
fig = plt.figure(figsize=(15, 5))
# Log-likelihood
ax = fig.add_subplot(1, 2, 1)
ax.plot(w0Vals, -ll, 'k-', label='Real nll')
ax.plot(w0Vals, offset  + w0InitDer*w0Vals, 'k:', label='linear approx.')
ax.plot(w0Init, nllInit, 'o', ms=10, color='k')
ax.set_xlabel('$w_0$')
ax.set_ylabel('Negative log-likelihood')
ax.legend()
# Log-likelihood decrease
ax = fig.add_subplot(1, 2, 2)
ax.plot(w0Vals[1:], realNllDecrease[1:] / expectedNllDecrease[1:], 'k-')
ax.set_xlabel('$w_0$')
ax.set_ylabel('nll / linear approx.');
# In[19]:
# Gradient descent parameters
eta = 0.1
alpha = 0.5
beta = 0.8
wUpdates = np.zeros([nIterations, 2])
wUpdates[0, :] = wInit
nllVals = np.zeros(nIterations)
nllVals[0] = negLogLikFun(X, wUpdates[0, :], y)
# Gradient descent with backtracking
for i in range(1, nIterations):
    wUpdates[i, :] = wUpdates[i-1, :]
    delta = negLogLikDerFun(X, wUpdates[i, :], y)
    tooLarge = True
    # Backtracking loop
    while tooLarge:
        wUpdates[i, :] -= eta*delta
        nllTmp = negLogLikFun(X, wUpdates[i, :], y)
        if nllTmp > nllVals[i-1] - alpha*eta*np.dot(delta, delta):
            wUpdates[i, :] += eta*delta
            eta *= beta
        else:
            tooLarge = False
            nllVals[i] = nllTmp
    
# Plotting
grayColors = getGrayColors(3)
fig = plt.figure(figsize=(25, 7))
ax = plt.subplot(1, 1, 1)
ax.set_aspect('equal')
# Negative log-likelihood
contourHandle = ax.contourf(W0, W1, -llVals, 50, cmap=cm.coolwarm)
# Gradient
ax.quiver(W0q, W1q, W0derNorm, W1derNorm, angles='xy', scale_units='xy', scale=30, width=2e-3)
# Gradient descent progress
ax.plot(wUpdates[:, 0], wUpdates[:, 1], '-o', ms=6, color='white', lw=3)
# Axes settings
ax.set_xlabel('$w_0$')
ax.set_ylabel('$w_1$');
cBarHandle = plt.colorbar(contourHandle)
cBarHandle.set_label('negative log-likelihood')
# In[20]:
# Gradient descent parameters
eta = 0.1
wUpdates = np.zeros([nIterations, 2])
wUpdates[0:2, :] = [-1.8, 0.85]
nllVals = np.zeros(nIterations)
nllVals[0:2] = negLogLikFun(X, wUpdates[0, :], y)
# Nesterov accelerated gradient with backtracking
for i in range(2, nIterations):
    v = wUpdates[i-1, :] + (i-2.)/(i+1)*(wUpdates[i-1, :]-wUpdates[i-2, :])
    delta = negLogLikDerFun(X, v, y)
    nllTmp = negLogLikFun(X, v , y)
    tooLarge = True
    # Backtracking loop
    while tooLarge:
        wUpdates[i, :] = v - eta*delta
        nllNew = negLogLikFun(X, wUpdates[i, :] , y)
        if nllNew > nllTmp - eta*np.dot(delta, delta)/2.:
            wUpdates[i, :] = wUpdates[i-1, :]
            eta *= beta
        else:
            tooLarge = False
            nllVals[i] = nllNew
# Plotting
grayColors = getGrayColors(3)
fig = plt.figure(figsize=(25, 7))
ax = plt.subplot(1, 1, 1)
ax.set_aspect('equal')
# Negative log-likelihood
contourHandle = ax.contourf(W0, W1, -llVals, 50, cmap=cm.coolwarm)
# Gradient
ax.quiver(W0q, W1q, W0derNorm, W1derNorm, angles='xy', scale_units='xy', scale=30, width=2e-3)
# Gradient descent progress
ax.plot(wUpdates[:, 0], wUpdates[:, 1], '-o', ms=6, color='white', lw=3)
# Axes settings
ax.set_xlabel('$w_0$')
ax.set_ylabel('$w_1$');
cBarHandle = plt.colorbar(contourHandle)
cBarHandle.set_label('negative log-likelihood')