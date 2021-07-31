#!/usr/bin/env python
# coding: utf-8
# In[1]:
# Panda es una libreria de manejo de datos
import pandas
# Matplotlib es una libreria de gráficos
import matplotlib.pyplot as matPlt
# Numpy es una librería que provee de objetos de n-dimensiones
import numpy
# Hace el grafico en la misma ventana
get_ipython().run_line_magic('matplotlib', 'inline')
# In[2]:
# Se cargan los datos de PIMA
dataFrame = pandas.read_csv("../data/pima-data.csv")
# In[3]:
# Shape indica las filas y columnas de la data recien cargada
dataFrame.shape
# In[4]:
# Muestra las primeras filas de datos
dataFrame.head(6)
# In[5]:
# Muestra las ultimas filas de datos
dataFrame.tail(4)
# In[6]:
# Revisamos si existen datos nulos, 
# la funcion devuelve True si existen valores nulos
# o False si no existen
dataFrame.isnull().values.any()
# In[28]:
def plot_corr(dataFrame, size=11):
    
    # Funcion que realiza correlaciones de dataFrame
    corr = dataFrame.corr()
    
    # Retorna los axes de las posiciones de los segmentos 
    # dentro del grafico
    # ref: https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.subplot
    fig, ax = matPlt.subplots(figsize=(size, size)) 
    
    # Despliega una matriz desde un arreglo
    # ref: https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.matshow
    ax.matshow(corr)
    
    # Dibuja los nombres de series en el gráfico
    # https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.xticks
    matPlt.xticks(range(len(corr.columns)), corr.columns)
    matPlt.yticks(range(len(corr.columns)), corr.columns)
# In[19]:
plot_corr(dataFrame)
# In[22]:
dataFrame.corr()
# In[24]:
dataFrame.head(8)
# In[25]:
del dataFrame['skin']
# In[26]:
dataFrame.head()
# In[29]:
plot_corr(dataFrame)
# In[30]:
dataFrame.head()
# In[35]:
diabetes_map = {True: 1, False: 0}
# In[36]:
dataFrame['diabetes'] = dataFrame['diabetes'].map(diabetes_map)
# In[37]:
dataFrame.head()