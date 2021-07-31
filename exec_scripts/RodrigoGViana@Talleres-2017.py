#!/usr/bin/env python
# coding: utf-8
# In[3]:
import matplotlib.pyplot as plt
import numpy as np
# In[4]:
X = [89.1, 89.8, 92, 91.5, 90.1, 91, 89.5, 91.8, 88.5, 86.7, 87.9, 89.9, 91.7, 90.3, 91.8, 88, 91.5, 91.1, 88.9, 90.8]
Y = [2116, 2984, 1531, 1380, 2717, 2545, 2004, 1611, 3477, 4814, 3860, 1827, 1947, 3071, 1594, 4015, 2059, 1975, 2880, 2352]
X = np.array(X)
Y = np.array(Y)
# In[26]:
plt.scatter(X,Y, s=100*2)
plt.xlabel('Rendimiento de pruebas (yield)')
plt.ylabel('Desperdicio (scrap)')
plt.show()
# In[30]:
r = np.corrcoef(X,Y)
print(('El coeficiente de correlación es {}').format(r[0][1]))
# In[31]:
plt.hist(X)
plt.xlabel('Rendimiento')
plt.ylabel('Frecuencias')
plt.show()
# In[32]:
plt.hist(Y, cumulative=True, color='darkgrey')
plt.xlabel('Desperdicio')
plt.ylabel('Frecuencias acumuladas')
plt.show()