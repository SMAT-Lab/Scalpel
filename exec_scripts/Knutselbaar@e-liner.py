#!/usr/bin/env python
# coding: utf-8
# In[1]:
import math
def bepaal_hoeken(x, y, l=10, x0=0, y0=0):
    if x-x0 == 0:
        a = math.pi/2
    else:
        a = math.atan((y-y0)/(x-x0))
    L = math.sqrt( math.pow(x-x0,2) + math.pow(y-y0,2) )
    B = L/2
    b = math.acos(B/l)
    if y < y0 or x < x0:
        a = a + math.pi
    return (a,b)
bepaal_hoeken(4,5)  # resultaat in radialen
# In[2]:
get_ipython().run_line_magic('matplotlib', 'inline')
# In[3]:
import matplotlib.pyplot as plt
import numpy as np
# In[4]:
def teken_ruit(x, y, l=10, x0=0, y0=0):
    (a,b) = bepaal_hoeken(x, y, l, x0, y0)
    x1 = math.cos(a+b)*l
    y1 = math.sin(a+b)*l
    x2 = math.cos(a-b)*l
    y2 = math.sin(a-b)*l
    plt.axis('equal')
    _ = plt.plot([x0,x1,x,x2,x0],[y0,y1,y,y2,y0])
# In[5]:
teken_ruit(5,5)     # blauw
teken_ruit(10,10)   # oranje
teken_ruit(14,14)   # groen
teken_ruit(1,5)     # rood
teken_ruit(5,1)     # paars
teken_ruit(1,1)     # bruin
# In[6]:
teken_ruit(19.5,0)
teken_ruit(0,19.5)
teken_ruit(-19.5,0)
cirkel = plt.Circle((0, 0), 19.5, color='black', fill=False)
_= plt.gcf().gca().add_artist(cirkel)
# In[7]:
def bepaal_dubbele_hoeken(x, y, l=10, d=4):
    (a,b) = bepaal_hoeken(x, y, l, -d/2, 0)
    hoek1 = a+b
    (a,b) = bepaal_hoeken(x, y, l,  d/2, 0)
    hoek2 = a-b
    return (hoek1,hoek2)
bepaal_dubbele_hoeken(10,10)  # resultaat in radialen
# In[8]:
def teken_armen(x, y, l=10, d=4):
    (hoek1, hoek2) = bepaal_dubbele_hoeken(x, y, l, d)
    x1 = math.cos(hoek1)*l - d/2
    y1 = math.sin(hoek1)*l
    x2 = math.cos(hoek2)*l + d/2
    y2 = math.sin(hoek2)*l
    plt.axis('equal')
    _ = plt.plot([-d/2,x1,x,x2,d/2],[0,y1,y,y2,0])
# In[9]:
teken_armen( 5, 5)     # blauw
teken_armen( 9,10)     # oranje
teken_armen(13,13)     # groen
teken_armen( 1, 8)     # rood
teken_armen( 5, 1)     # paars
# In[10]:
teken_armen(17.5,0)
teken_armen(0,17.5)
teken_armen(-17.5,0)
cirkel = plt.Circle((0, 0), 17.5, color='black', fill=False)
_= plt.gcf().gca().add_artist(cirkel)