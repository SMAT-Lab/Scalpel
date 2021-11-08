#!/usr/bin/env python
# coding: utf-8
# In[144]:
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import sympy 
#%matplotlib notebook
get_ipython().run_line_magic('matplotlib', 'inline')
# In[145]:
y, x = np.ogrid[-1:2:100j, -1:1:100j]
plt.contour(x.ravel(), 
            y.ravel(), 
            x**2 + (y-((x**2)**(1.0/3)))**2, 
            [1],
            colors='red',)
plt.axis('equal')
plt.show()  
# In[155]:
def fun(s,t):
    R = s[0]
    J = s[1]
    a = 2
    b = 8
    c=-5
    d = -3
    Rdot = a*R + b*J
    Jdot = c*R + d*J
    return [Rdot, Jdot]
a = 2;b = 8;c = -5;d = -3
A = np.matrix([[a, b],[c,d]])
e_vals, e_vecs = eig(A) 
print(e_vals) # checking the eigenvalues- we have both complex and negative
# Solving the system of ODE
t = np.arange(0,10,0.01) # Setting time between 0 and 10 at interval of 0.01
init1 = [1,1]  # setting initial condition i.e., the first impression
sol1 = odeint(fun, init1, t) # integrating 
plt.plot(sol1[:,0], sol1[:,1], color = 'r')  # streamplot is a better plot 
x = np.linspace(-2,2,50) 
y = np.linspace(-2,2,50)
xx,yy = np.meshgrid(x,y)
plt.quiver(xx, yy, a*xx+b*yy, c*xx + d*yy)    
plt.xlabel('R(t)')
plt.ylabel('J(t)')   
plt.savefig("fig1-a.png")  
# In[157]:
def fun(s,t):
    P = s[0]
    C = s[1]
    a = 5
    b = 2
    c = 8
    d = 4
    Rdot = a*P + b*C
    Jdot = c*P + d*C
    return [Rdot, Jdot]
t = np.arange(0,10,0.01)
init1 = [1,-1]
sol1 = odeint(fun, init1, t) 
a = 5;b = 2;c = 8;d = 4
A = np.matrix([[a, b],[c,d]])
e_vals, e_vecs = eig(A) 
print(e_vals) # checking the eigenvalues- we have both real and positive
x = np.linspace(-1,1,20) 
y = np.linspace(-1,1,20)
xx,yy = np.meshgrid(x,y)
plt.streamplot(xx, yy, a*xx+b*yy, c*xx + d*yy, density=1,color='r')      
#plt.quiver(xx, yy, a*xx+b*yy, c*xx + d*yy) 
plt.xlabel('R(t)')
plt.ylabel('J(t)')   
plt.savefig("fig1-b,.png") 
# In[158]:
def fun(s,t):
    R = s[0]
    J = s[1]
    a = 2
    b = -8
    c = -5
    d = -3
    Rdot = a*R + b*J
    Jdot = c*R + d*J
    return [Rdot, Jdot]
t = np.arange(-10,10,0.01)
init1 = [1,-1]
sol1 = odeint(fun, init1, t) 
#plt.plot(sol1[:,0], sol1[:,1])  
a = 2;b = -8;c = -5;d = -3
A = np.matrix([[a, b],[c,d]])
e_vals, e_vecs = eig(A) 
print(e_vals) # checking the eigenvalues- we have both real and opposite in signs
x = np.linspace(-1,1,20) 
y = np.linspace(-1,1,20)
xx,yy = np.meshgrid(x,y)
plt.streamplot(xx, yy, a*xx+b*yy, c*xx + d*yy, density=1,color='r')      
#plt.quiver(xx, yy, a*xx+b*yy, c*xx + d*yy) 
plt.xlabel('R(t)')
plt.ylabel('J(t)')   
plt.savefig("fig1-c.png")
# In[77]:
def fun(s,t):
    R = s[0]
    J = s[1]
    a = 2
    b = 8
    c = -5
    d = -3
    Rdot = a*R + b*J
    Jdot = c*R + d*J
    return [Rdot, Jdot]
t = np.arange(0,10,0.01)
init1 = [5,2]
#init2 = [0,0]
sol1 = odeint(fun, init1, t) 
#sol2 = odeint(fun, init2, t) 
plt.plot(sol1[:,0], sol1[:,1], color='g')   
#plt.plot(sol2[:,0], sol2[:,1])    
# In[159]:
def fun(s,t):
    R = s[0]
    J= s[1]
    a = -2
    b = 8
    c = -5
    d = 2
    Rdot = a*R + b*J
    Jdot = c*R + d*J
    return [Rdot, Jdot]
t = np.arange(0,10,0.01)
init1 = [1,-1]
sol1 = odeint(fun, init1, t) 
plt.plot(sol1[:,0], sol1[:,1])  
 
a = -2; b=8
c = -8; d=2
A = np.matrix([[a, b],[c,d]])
e_vals, e_vecs = eig(A) 
print(e_vals) # checking the eigenvalues- we have both real and opposite in signs
# Nullclines plots
Rn = np.linspace(-2,2, 50)
ax = plt.plot(Rn, -a/b*Rn) 
plt.plot(Rn, -c/d*Rn) 
ax = plt.gca() 
ax.xaxis.grid(True) 
ax.yaxis.grid(True) 
plt.xlabel("Evolving of " r'$\mathbf{R }$' "'s love for " r'$\mathbf{J}$' " over time") 
plt.ylabel("Evolving of " r'$\mathbf{J}$' "'s love for " r'$\mathbf{R}$' " over time") 
#plt.title(" A solution of " r'$\frac{dR}{dt} = aR + bJ$' " and " r'$\frac{dJ}{dt} = cR + dJ$' " system ")  
ax.annotate("P loves but C do not, i.e.  $a = -d$ ", xy=(-2, 3), xytext=(-1.8, 5))
ax.annotate('No matter what, the relation will not hit the intersection.', xy=(-2, 3), xytext=(-1.8, 4.)) 
plt.savefig("fig2-a.png") 
# In[161]:
def fun(s,t):
    R = s[0]
    J = s[1]
    a = 2
    b = -8
    c = 8
    d = -2
    Rdot = a*R + b*J
    Jdot = c*R + d*J
    return [Rdot, Jdot]
t = np.arange(-10,10,0.01)
init1 = [1,-1]
sol1 = odeint(fun, init1, t) 
#plt.plot(sol1[:,0], sol1[:,1])  
a = 8; b=2
c = -2; d=-8
A = np.matrix([[a, b],[c,d]])
e_vals, e_vecs = eig(A) 
print(e_vals) # checking the eigenvalues- we have both real and opposite in signs
x = np.linspace(-1,1,20) 
y = np.linspace(-1,1,20)
xx,yy = np.meshgrid(x,y)
plt.streamplot(xx, yy, a*xx+b*yy, c*xx + d*yy, density=1,color='r')    
plt.xlabel("Evolving of " r'$\mathbf{R }$' "'s love for " r'$\mathbf{J}$' " over time") 
plt.ylabel("Evolving of " r'$\mathbf{J}$' "'s love for " r'$\mathbf{R}$' " over time") 
#plt.quiver(xx, yy, a*xx+b*yy, c*xx + d*yy) 
plt.savefig("fig2-b.png") 
# In[121]:
def fun(s,t):
    P = s[0]
    C = s[1]
    a = 2
    b = -8
    c = -5
    d = -3
    Rdot = a*P + b*C
    Jdot = c*P + d*C
    return [Rdot, Jdot]
t = np.arange(-10,10,0.01)
init1 = [1,-1]
sol1 = odeint(fun, init1, t) 
plt.figure() 
plt.subplot(121)
plt.plot(sol1[:,0], sol1[:,1])  
a = 2;b = -8;c = -5;d = -3
x = np.linspace(-1,1,20) 
y = np.linspace(-1,1,20)
xx,yy = np.meshgrid(x,y)
plt.subplot(122)
plt.streamplot(xx, yy, a*xx+b*yy, c*xx + d*yy, density=1,color='r')      
#plt.quiver(xx, yy, a*xx+b*yy, c*xx + d*yy) 
# In[37]:
X, Y = np.meshgrid(np.arange(0, 2 * np.pi, .2), np.arange(0, 2 * np.pi, .2))
U = np.cos(X)
V = np.sin(Y)
# 1
plt.figure()
Q = plt.quiver(U, V)