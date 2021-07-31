#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
# In[116]:
N = 10
X = np.array([
    np.ones(N),
    np.random.random_sample(N),
]).T
Y = X[:,1] + np.random.normal(scale=0.1, size=N)
# In[118]:
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(X[:, 1], Y)
# In[119]:
hat_matrix = X @ np.linalg.inv((X.T @ X)) @ X.T
# In[120]:
X_cross = np.linalg.inv(X.T @ X) @ X.T
# In[126]:
betas = X_cross @ Y
betas
# In[124]:
y_hat = hat_matrix @ Y
# In[140]:
np.isclose((hat_matrix @ hat_matrix), hat_matrix).sum()
# In[141]:
np.isclose(hat_matrix.T, hat_matrix).sum()
# In[144]:
hat_matrix.diagonal().sum()
# In[128]:
plt.scatter(X[:, 1], Y, color="black")
plt.scatter(X[:, 1], y_hat, color="blue")
plt.plot([0, 1], [betas[0], betas[0] + betas[1]])