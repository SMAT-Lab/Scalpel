#!/usr/bin/env python
# coding: utf-8
# In[7]:
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy
from matplotlib import pylab
plt.rcParams["figure.figsize"] = (25, 16)
plt.rcParams['font.size'] = 18.0
Resistor100k = pd.read_csv('data/Resistor 100k.csv')
Resistor100k = Resistor100k[3:31]
Resistor100k["Time"] = Resistor100k["Time"].apply(lambda x: x-0.3)
plt.figure(1)
plt.plot(Resistor100k["Time"],Resistor100k["Potential"],'o', Resistor100k["Time"],Resistor100k["Potential"])
pylab.title('Gráfico do potencial pelo tempo usando o resistor de 100k')
plt.xlabel("Tempo")
plt.ylabel("Potencial")
plt.figure(2)
slope, intercept, r_value, p_value, std_err = stats.linregress(Resistor100k["Time"],Resistor100k["Potential"].apply(numpy.log))
line = slope*Resistor100k["Time"]+intercept
plt.plot(Resistor100k["Time"],Resistor100k["Potential"].apply(numpy.log),'o', Resistor100k["Time"], line)
pylab.title('Gráfico do potencial pelo tempo usando o resistor de 100k (Linearizado)')
ax = plt.gca()
fig = plt.gcf()
plt.xlabel("Tempo")
plt.ylabel("Potencial")
plt.show()
# In[5]:
Resistor47k = pd.read_csv('data/Resistor 47k.csv')
Resistor47k = Resistor47k[2:22]
Resistor47k["Time"] = Resistor47k["Time"].apply(lambda x: x-0.2)
plt.figure(1)
plt.plot(Resistor47k["Time"],Resistor47k["Potential"],'o', Resistor47k["Time"],Resistor47k["Potential"])
pylab.title('Gráfico do potencial pelo tempo usando o resistor de 47k')
plt.xlabel("Tempo")
plt.ylabel("Potencial")
plt.figure(2)
slope, intercept, r_value, p_value, std_err = stats.linregress(Resistor47k["Time"],Resistor47k["Potential"].apply(numpy.log))
line = slope*Resistor47k["Time"]+intercept
plt.plot(Resistor47k["Time"],Resistor47k["Potential"].apply(numpy.log),'o', Resistor47k["Time"], line)
pylab.title('Gráfico do potencial pelo tempo usando o resistor de 47k (Linearizado)')
ax = plt.gca()
fig = plt.gcf()
plt.xlabel("Tempo")
plt.ylabel("Potencial")
plt.show()
# In[6]:
Resistor22k = pd.read_csv('data/Resistor 22k.csv')
Resistor22k = Resistor22k[3:18]
Resistor22k["Time"] = Resistor22k["Time"].apply(lambda x: x-0.3)
plt.figure(1)
plt.plot(Resistor22k["Time"],Resistor22k["Potential"],'o', Resistor22k["Time"],Resistor22k["Potential"])
pylab.title('Gráfico do potencial pelo tempo usando o resistor de 22k')
plt.xlabel("Tempo")
plt.ylabel("Potencial")
plt.figure(2)
slope, intercept, r_value, p_value, std_err = stats.linregress(Resistor22k["Time"],Resistor22k["Potential"].apply(numpy.log))
line = slope*Resistor22k["Time"]+intercept
plt.plot(Resistor22k["Time"],Resistor22k["Potential"].apply(numpy.log),'o', Resistor22k["Time"], line)
pylab.title('Gráfico do potencial pelo tempo usando o resistor de 22k (Linearizado)')
ax = plt.gca()
fig = plt.gcf()
plt.xlabel("Tempo")
plt.ylabel("Potencial")
plt.show()
# In[17]:
slope, intercept, r_value, p_value, std_err = stats.linregress(Resistor22k["Time"],Resistor22k["Potential"].apply(numpy.log))
line1 = slope*Resistor22k["Time"]+intercept
plt.plot(Resistor22k["Time"], line1,label="Resistor 22k")
ax1 = plt.gca()
fig = plt.gcf()
slope, intercept, r_value, p_value, std_err = stats.linregress(Resistor47k["Time"],Resistor47k["Potential"].apply(numpy.log))
line2 = slope*Resistor47k["Time"]+intercept
plt.plot(Resistor47k["Time"], line2,label="Resistor 47k")
ax2 = plt.gca()
fig = plt.gcf()
slope, intercept, r_value, p_value, std_err = stats.linregress(Resistor100k["Time"],Resistor100k["Potential"].apply(numpy.log))
line3 = slope*Resistor100k["Time"]+intercept
plt.plot(Resistor100k["Time"], line3,label="Resistor 100k")
pylab.title('Gráfico do potencial pelo tempo de todos os resistores (Linearizado)')
ax3 = plt.gca()
fig = plt.gcf()
plt.legend()
plt.xlabel("Tempo")
plt.ylabel("Potencial")
plt.show()