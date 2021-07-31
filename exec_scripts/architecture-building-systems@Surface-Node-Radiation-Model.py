#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import pandas as pd
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# In[2]:
# Import csv (csv files containing the coordinates of the subsurfaces of the two main surfaces)
filename = 'Radiator_Low_Res.csv'
#filename = 'Radiator_Mid_Res.csv'
#filename = 'Radiator_High_Res.csv'
with open(filename, 'rU') as p:
        my_list = [[float(x) for x in rec] for rec in csv.reader(p, delimiter=',')]
lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
subsurfaces1 = []
for i in range(0,len(my_list)):
    subsurfaces1.append(lol(my_list[i],3))
filename = 'Body_Low_Res.csv'
#filename = 'Body_Mid_Res.csv'
#filename = 'Body_High_Res.csv'
with open(filename, 'rU') as p:
        my_list = [[float(x) for x in rec] for rec in csv.reader(p, delimiter=',')]
subsurfaces2 = []
for i in range(0,len(my_list)):
    subsurfaces2.append(lol(my_list[i],3))
# In[32]:
x = []; x1 = [] 
y =[]; y1 = [] 
z = []; z1 = []
for s1 in subsurfaces1:
    for ss1 in s1:
        x.append(ss1[0])
        y.append(ss1[1])
        z.append(ss1[2])
for s2 in subsurfaces2:
    for ss2 in s2:
        x1.append(ss2[0])
        y1.append(ss2[1])
        z1.append(ss2[2])
# In[33]:
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x, y, z, zdir='z')
ax.plot(x1, y1, z1, zdir='z')
ax.legend()
ax.set_xlim3d(-1000, 1000)
ax.set_ylim3d(-500, 1000)
ax.set_zlim3d(-1000, 1000)
plt.show()
# In[3]:
# Geometric Functions
def midpt_triangle(s): # returns centre of polygon
    return [x/3 for x in (sum(i) for i in zip(*s))]
def midpt_twopts(a,b):
    return [(x + y)/2 for x, y in zip(a, b)]
def vector_vertices(a,b): # returns vector of edge connecting 2 vertices
    return [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
def mag_vector(x): # returns magnitude of vector
    return np.sqrt(np.sum(np.square(x)))
def area_triangle(s): # returns area of triangle
    b = mag_vector(vector_vertices(s[0],s[1]))
    mpt = midpt_twopts(s[0],s[1])
    h = mag_vector(vector_vertices(s[2],mpt))
    return 0.5*b*h
def normal_vector(s): # returns vector normal to surface defined by 3 points
    ab = vector_vertices(s[0],s[1])
    bc = vector_vertices(s[1],s[2])
    return [ab[1]*bc[2]-ab[2]*bc[1],ab[0]*bc[2]-ab[2]*bc[0],ab[0]*bc[1]-ab[1]*bc[0]]
def angle_incident(vector1,vector2): #returns angle between 2 vectors
    return np.arccos(sum([a*b for a,b in zip(vector1,vector2)])/(mag_vector(vector1)* mag_vector(vector2)))
def form_factor(A1,A2,theta1,theta2,r,b): # returns form factor of surface 2 wrt surface 1
    return abs(np.cos(theta1))*abs(np.cos(theta2))*A1*A2*b/(3.14*np.square(r))
# In[4]:
# Vector operations
def dot(A,B):
    return A[0] * B[0] + A[1]*B[1] + A[2]*B[2]
def cross(A,B):
    return [A[1]*B[2]-A[2]*B[1], A[0]*B[2]-A[2]*B[0], A[0]*B[1]-A[1]*B[0]]
# math_geom_c method
def add_v3v3(v0, v1):
    return (
        v0[0] + v1[0],
        v0[1] + v1[1],
        v0[2] + v1[2],
        )
def sub_v3v3(v0, v1):
    return (
        v0[0] - v1[0],
        v0[1] - v1[1],
        v0[2] - v1[2],
        )
def dot_v3v3(v0, v1):
    return (
        (v0[0] * v1[0]) +
        (v0[1] * v1[1]) +
        (v0[2] * v1[2])
        )
def len_squared_v3(v0):
    return dot_v3v3(v0, v0)
def mul_v3_fl(v0, f):
    return (
        v0[0] * f,
        v0[1] * f,
        v0[2] * f,
        )
# In[5]:
# blocked surfaces
def block_math(s, sa, sb):
    epsilon = 1e-6
    p0 = midpt_triangle(sa)
    p1 = midpt_triangle(sb)
    plane = cross(sub_v3v3(s[1], s[0]), sub_v3v3(s[2], s[0]))
    plane.append(-dot_v3v3(plane, s[0]))
    # def isect_line_plane_v3_4d(p0, p1, plane, epsilon=1e-6):
    u = sub_v3v3(p1, p0)
    dot = dot_v3v3(plane, u)
    if abs(dot) > epsilon:
        p_co = mul_v3_fl(plane, -plane[3] / len_squared_v3(plane))
        w = sub_v3v3(p0, p_co)
        fac = -dot_v3v3(plane, w) / dot
        u = mul_v3_fl(u, fac)
        i = add_v3v3(p0, u)
        mcheck = dot_v3v3(sub_v3v3(i, p0), sub_v3v3(p1, i))
        # Compute vectors
        v0 = sub_v3v3(s[2],s[0])
        v1 = sub_v3v3(s[1],s[0])
        v2 = sub_v3v3(i,s[0])
        # Compute dot products
        dot00 = dot_v3v3(v0, v0)
        dot01 = dot_v3v3(v0, v1)
        dot02 = dot_v3v3(v0, v2)
        dot11 = dot_v3v3(v1, v1)
        dot12 = dot_v3v3(v1, v2)
        # Compute barycentric coordinates
        invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom
        # Check if point is in triangle
        if u >= 0 and v >= 0 and (u + v < 1) and mcheck> -epsilon:
            return 0 #'intersect'
        else:
            return 1 #'no intersect'
    else:
        return 1 #'plane parallel to ray, hence no intersect'
# In[6]:
#  define empty lists to populate with calculation parameters/outputs
f = []
theta1_arch = []
theta2_arch = []
R_arch = []
Rmag_arch =[]
btotal_arch = []
subsurfaces1_arch = []
subsurfaces2_arch = []
# In[8]:
#  form factor calculation
for s1 in subsurfaces1:
    x = list(subsurfaces1)
    x.remove(s1)
    for s2 in subsurfaces2:
        y = list(subsurfaces2)
        y.remove(s2)
        b_arch = []
        for s in (x + y):
            b1 = block_math(s, s1, s2)
            b_arch.append(b1)
        b = np.prod(np.array(b_arch))
        # b = 1
        R = vector_vertices(midpt_triangle(s1), midpt_triangle(s2))
        Rmag = mag_vector(R)
        theta1 = angle_incident(R, normal_vector(s1))
        theta2 = angle_incident(R, normal_vector(s2))
        f.append(form_factor(area_triangle(s1),area_triangle(s2),theta1,theta2,Rmag,b))
        R_arch.append(R)
        Rmag_arch.append(Rmag)
        theta1_arch.append(theta1)
        theta2_arch.append(theta2)
        btotal_arch.append(b)
        subsurfaces1_arch.append(s1)
        subsurfaces2_arch.append(s2)
# In[9]:
# Calculate area of primary polygon
A1 = 0
for item in subsurfaces1: A1 = A1 + area_triangle(item)
# Calculate form factor
result = (sum(f))/A1
print("The distance vectors are ", R_arch)
print("The distances are ", Rmag_arch)
print("The theta1s are ", theta1_arch)
print("The theta2s are ", theta2_arch)
print("The final view factor is ", result)
# In[11]:
# visualization
block1 = [a*b for a,b in zip(subsurfaces1_arch,btotal_arch)]
block1 = list(filter(None, block1))
block2 = [a*b for a,b in zip(subsurfaces2_arch,btotal_arch)]
block2 = list(filter(None, block2))
blocked_surfaces1 = [x for x in subsurfaces1 if x not in block1]
blocked_surfaces2 = [x for x in subsurfaces2 if x not in block2]
x1 = []; x1b = []; y1 =[]; y1b = []; z1 = []; z1b = []
x2 = []; x2b = []; y2 =[]; y2b = []; z2 = []; z2b = []
for s1 in subsurfaces1:
    for ss1 in s1:
        x1.append(ss1[0])
        y1.append(ss1[1])
        z1.append(ss1[2])
for s1b in blocked_surfaces1:
    for ss1b in s1b:
        x1b.append(ss1b[0])
        y1b.append(ss1b[1])
        z1b.append(ss1b[2])
for s2 in subsurfaces2:
    for ss2 in s2:
        x2.append(ss2[0])
        y2.append(ss2[1])
        z2.append(ss2[2])
#
for s2b in blocked_surfaces2:
    for ss2b in s2b:
        x2b.append(ss2b[0])
        y2b.append(ss2b[1])
        z2b.append(ss2b[2])
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x1, y1, z1, zdir='z')
ax.plot(x1b, y1b, z1b, zdir='z')
ax.plot(x2, y2, z2, zdir='z')
ax.plot(x2b, y2b, z2b, zdir='z')
plt.show()
# In[12]:
# Gebhart Factor Calculation
# Body 1 is sandprint; Body 2 is human body
E1 = 0.90 # emissivity of sand
E2 = 0.98 # emissivity of human body
A2 = 0
for item in subsurfaces2: A2 = A2 + area_triangle(item)
A1 = A1/1000000
A2 = A2/1000000
FF12 = result
B12 = FF12*E2*A2/(1-(FF12**2)*A1*(1-E1)*(1-E2))
# In[13]:
# heat transfer and material constants
sigma = 5.67*10**-8  # stefan-boltzmann constant [W/m2/K4]
hc = 10.45 # convective heat transfer coefficient of air [W/m2/K]
c2 = 3500 # heat capacitance of human body [J/kg/K]
ca = 1005 # capacitance of air [J/kg/K]
m2 = 65 # weight of human [kg]
va = 5*5*5 # volume of air [m3]
rhoa = 1.29 # density of air [kg/m3]
ma = va*rhoa # weight of air [kg]
# In[14]:
# initialize variables
i = 0
T1 = 273 + 45 # temperature of sandprint [K]
T2 = 273 + 34 # temperature of human surface [K]
Ta = 273 + 20 # temperature of air [K]
# In[15]:
# empty lists to store timeseries
q12rarch = []
qa1carch = []
qa2carch = []
q2arch = []
qaarch = []
T1arch = []
T2arch = []
Taarch = []
iarch = []
# In[16]:
# run RC model
while i < 7200:
    q12r = E1*A1*B12*sigma*(T1**4-T2**4)
    qa2c = hc*A2*(T2-Ta)
    qa1c = hc*A1*(T1-Ta)
    q2 = q12r - qa2c
    qa = qa1c + qa2c
    T2 = q2/(m2*c2) + T2
    Ta = qa/(ma*ca) + Ta
    q12rarch.append(q12r)
    qa1carch.append(qa1c)
    qa2carch.append(qa2c)
    q2arch.append(q2)
    qaarch.append(qa)
    T1arch.append(T1)
    T2arch.append(T2)
    Taarch.append(Ta)
    iarch.append(i)
    i = i + 1
# In[17]:
# plots
plt.figure(1)
fig, axes = plt.subplots(nrows=2, ncols=2)
plt.subplot(221)
plt.plot(iarch,Taarch,'b-')
plt.title('T_air [K]')
plt.subplot(222)
plt.plot(iarch,T2arch,'g-')
plt.title('T_surf_human [K]')
plt.subplot(223)
plt.plot(iarch,qa1carch,'b-')
plt.title('Qcon_heater_air [W]')
plt.xlabel('Time [s]')
plt.subplot(224)
plt.plot(iarch,q12rarch,'g-')
plt.title('Qrad_heater_human [W]')
plt.xlabel('Time [s]')
fig.tight_layout()
plt.show()