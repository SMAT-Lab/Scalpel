#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
# Each element must be of the same type.
intarray = np.array([1, 2, 3, 4])
intarray.dtype
# In[2]:
floatarray = np.array([1.0, 2.0, 3.0, 4.0])
floatarray.dtype
# In[3]:
# Numpy will try to coerce elements to the same datatype:
mixedarray = np.array([1, 2.0, 3, np.pi])
mixedarray.dtype
# In[4]:
# If you force it to coerce too much you end up with "object" as a dtype, which is not useful. Stick to numbers.
dont_do_this = np.array([1, False, "a string", object()])
dont_do_this.dtype
# In[5]:
# You can specify the dtype when creating the ndarray, otherwise it will be inferred, defaulting to float64
floats = np.array([0, 1, 2], dtype="float64")
floats.dtype
# In[6]:
def describe_array(name, a):
    print(name)
    print(a)
    print("Array ndim: ", a.ndim)
    print("Array shape: ", a.shape)
    print("Array size: ", a.size)
    print()
describe_array("1 row, 3 columns", np.array([1, 2, 3]))
describe_array("2 rows, 3 columns", np.array([[1, 2, 3], [4, 5, 6]]))
describe_array("3 rows, 2 columns", np.array([[1, 2], [3, 4], [5, 6]]))
describe_array("2 faces, 3 rows, 1 column", np.array([[[1], [2], [3]], [[4], [5], [6]]]))
# In[7]:
# arrays can be reshaped after they are created:
a = np.array([1, 2, 3, 4, 5, 6])
a
# In[8]:
# two rows, 3 columns
a.reshape(2, 3)
# In[9]:
# np.arange([start,], stop[, step])
np.arange(10)
# In[10]:
np.arange(100, 90, -1)
# In[11]:
# np.zeros(shape) where `shape` is a tuple.
# e.g. 1 row, 3 columns
np.zeros((1, 3))
# In[12]:
# or 2 faces, 5 rows, 2 columns
np.zeros((2, 5, 2))
# In[13]:
# np.eye(rows, columns=None, k=0)
np.eye(4)
# In[14]:
# np.random.randint(low, high, shape)
np.random.randint(0, 10, (3, 3))
# In[15]:
# np.random.normal(mean, stdev, shape)
np.random.normal(0, 1, (4, 4))
# In[16]:
a = np.arange(0, 10)
print(a)
# In[17]:
a + 10
# In[18]:
a * 2
# In[19]:
# Let's create a python list and an array, each with 10 million integers.
big_list = list(range(10000000))
big_array = np.arange(10000000)
# In[20]:
# See how long it takes to get a new list containing the square of each element from big_list
get_ipython().run_line_magic('timeit', 'big_list_squared = [i * i for i in big_list]')
# In[21]:
# See how long it takes to get a new array containing the square of each element from big_array
get_ipython().run_line_magic('timeit', 'big_array_squared = big_array * big_array')
# In[22]:
import math
get_ipython().run_line_magic('timeit', 'big_list_sines = [math.sin(i) for i in big_list]')
# In[23]:
# numpy ufuncs provide vectorized operations that go beyond simple arithmetic.
# np.sin() calculates the sine of each element in the passed-in array.
get_ipython().run_line_magic('timeit', 'big_array_sines = np.sin(big_array)')
# In[24]:
# And not only is the list slower, it also uses a more memory. Below is its size in mbytes.
import sys
sys.getsizeof(big_list) / 1024 / 1024
# In[25]:
# vs. the size of the array in mbytes
sys.getsizeof(big_array) / 1024 / 1024
# In[26]:
# Note there is a special function for the dot product, do not use the built-in '*' operator
a1 = np.arange(0, 9).reshape(3,3)
a2 = np.arange(10, 19).reshape(3,3)
print("a1:", repr(a1))
print()
print("a2:", repr(a2))
# In[27]:
# the * operator performs element-wise multiplication
a1 * a2
# In[28]:
# to get the dot product of a matrix and a vector:
a1.dot(a2[0])
# In[29]:
# or the dot product of two matrices:
a1.dot(a2)
# In[30]:
np.matmul(a1, a2)
# In[31]:
m1 = np.matrix(a1)
m2 = np.matrix(a2)
# In[32]:
m1 * m2
# In[33]:
a = np.array([10, 11, 12, 13, 14])
a[1:3]
# In[34]:
# slicing a multidimensional array:
a = np.arange(9).reshape(3, 3)
a
# In[35]:
# to get a scalar element value, specify its location in all dimensions (here, just row and column):
a[1, 1]
# In[36]:
# retrieve an entire row by index:
a[0]
# In[37]:
# retrieve an entire column by index (note the slice syntax to get all rows,
# then the index to specify which column to extract from each row)
a[:, 0]
# In[38]:
# to select a sub-matrix, use slice syntax to specify row and column locations.
# here, we get the bottom-left corner of the matrix:
# (all rows starting with the second row, and all columns but the last one)
a[1:, :2]
# In[39]:
# Get a slice of `a`, in this case the entire first row.
a = np.arange(10)
b = a[:]
b
# In[40]:
# Now let's change the last element from 9 to 90
a[-1] = 90
# In[41]:
# and we see that the value changes in the view as well.
b
# In[42]:
# to get a copy of an array, use the `copy` method:
a = np.arange(10)
b = a.copy()
b
# In[43]:
# because we used `copy` to create array `b`, changing a value in `a` will not affect `b`:
a[-1] = 90
b
# In[44]:
# boolean comparisons to arrays produce a "mask" array: an array of the same shape filled with boolean values
# indicating whether the item at that position in the original array meets the boolean condition.
a = np.random.randint(0, 10, (20))
print(a)
print(a > 5)
# In[45]:
# We can now use that "mask" array to select elements from an array with the same shape.
# for example, below will give us a new array with only the elements in `a` greater than 5.
# NB: in this case we get a copy of the original data, not a view like we would if we had sliced the array.
a[a > 5]
# In[46]:
# It's possible to chain multiple boolean tests together with the & and | operators
# (although the conditions must be in parentheses)
a[(a <= 2) | (a >= 8)]
# In[47]:
a = np.arange(18).reshape((2,3,3))
a
# In[48]:
# the `T` property of an ndarray provides easy access to the transpositions of all axes:
a.T
# In[49]:
# the `transpose` method lets us transpose axes in a particular order:
a.transpose((0, 2, 1))
# In[50]:
a1 = np.arange(3)
a2 = np.arange(3, 6)
# In[51]:
# stack "column-wise". This can also be done via the deprecated `np.hstack` function.
np.stack([a1, a2])
# In[52]:
# stack "row-wise", as the `np.vstack` function.
np.stack([a1, a2], axis=1)
# In[53]:
np.concatenate([a1, a2])
# In[54]:
with open('data.csv') as f:
    for row in f:
        print(row)
# In[55]:
data = np.loadtxt("data.csv", skiprows=1, delimiter=",")
# In[56]:
data
# In[57]:
data.dtype
# In[58]:
# By default, genfromtxt gives the same (two-dimensional) output.
np.genfromtxt("data.csv", skip_header=1, delimiter=",")
# In[59]:
# But if we specify `dtype=None` as an argument, it returns a one-dimensional array of "structured" arrays,
# where the data type for each element is determined automatically.
arr = np.genfromtxt("data.csv", dtype=None, skip_header=1, delimiter=",")
arr
# In[60]:
import numpy as np
import matplotlib.pyplot as plt
p = np.poly1d([3, 2, -1])
print('Show the constant')
print(p(0))
print('Print the roots of the polynomial')
print(p.roots)
print('Print the order of the polynomial')
print(p.order)
print('Create X-values')
x = np.linspace(0, 1, 20)
print('x values = ',x)
print('Create random y values about the curve')
y = np.cos(x) + 0.3*np.random.rand(20)
print('y values = ',y)
print('Fit the data using polyfit and constuct a polynomial from the fit')
p = np.poly1d(np.polyfit(x, y, 3))
t = np.linspace(0, 1, 200)
print('plot the data and the fit')
plt.plot(x, y, 'o', t, p(t), '-')
plt.show()
# In[61]:
import numpy as np
A=np.array([[1,2],[3,4]])
print(A)
result_one=np.linalg.norm(A)
result_two=np.linalg.norm(A,'fro') # frobenius norm
result_three=np.linalg.norm(A,1) # L1 norm (max column sum)
result_four=np.linalg.norm(A,-1)
result_five=np.linalg.norm(A,np.inf) # L inf norm (max row sum)
print("Norm of the array",result_one)
print("Frobenius Norm is the default ||A||=[\sum_{i}{j} abs(a_{ij})^2]^[1/2]=",result_two)
print("max(sum(abs(x), axis=0))=", result_three)
print("min(sum(abs(x), axis=0))=",result_four)
print("max(abs(x))=",result_five)
# In[62]:
import numpy as np
A = np.array([[1,2,3],[3,4,6],[7,8,9]])
print(A)
determ=np.linalg.det(A)
print(determ)
# In[63]:
import numpy as np
#Solve the linear system 3x1+x2+2x3=9 x1+2x2+x3=8 2x2-1x3=2
A = np.array([[3,1,2], [1,2,1],[0,2,-1]])
b = np.array([9,8,2])
x = np.linalg.solve(A, b)
print(x)
np.allclose(np.dot(A, x), b)
#Returns True if two arrays are element-wise equal within a tolerance.
# In[64]:
import numpy as np
#using the mat functions
#make an array from for a list of lists
A = np.mat([[3, 1, 4+0.1j], [1, 5-2j, 9], [2, 6+2j, 5]])
print('Complex Array A')
print(A)
print(type(A), A.dtype, A.shape)
# In[65]:
A_tr=A.T
A_H=A.H
A_I=A.I
A_A=A.A
A_A1=A.A1
print('Transpose of A=')
print(A_tr)
print('Hermitian of A=')
print(A_H)
print('Inverse of A=')
print(A_I)
print('Standard ndarray=')
print(A_A)
print('One dimestional array of A=')
print(A_A1)
# In[66]:
#Verify the inverse
np.set_printoptions(precision = 2)
Atest=A*A.I
print(Atest)
# In[67]:
#define a column vector
b = np.mat('1; 2; 3')
# matrix multiply by vector
print('Vector b = ',b)
#multiply square matrix by vector
result=A*b
print("A*b=",result)
# returns a row vector
print('Compute b^T * A')
row_vector=b.T*A
print('Row vector = ', row_vector)
#turn back to 1-D array
one_d=(b.T*A).A1
print('1D array of the row vector = ',one_d)
# In[68]:
np.set_printoptions(precision = 6)
print("A = ",A)
print("b = ",b)
print('Solve as X=A^(-1)*b')
x=A.I*b
#solution x
print(x)
#verify
res=A*x-b
print('Residual = ',res)
#alternative
solution=np.linalg.solve(A, b)
print('linalg solution = ',solution)
# In[69]:
import numpy as np
import matplotlib.pyplot as plt
c1, c2 = 5.0, 2.0
i = np.r_[1:11]
xi = 0.1*i
yi = c1*np.exp(-xi) + c2*xi
zi = yi + 0.05 * np.max(yi) * np.random.randn(len(yi))
A = np.c_[np.exp(-xi)[:, np.newaxis], xi[:, np.newaxis]]
c, resid, rank, sigma = np.linalg.lstsq(A, zi) # solve using linalg.lsteq
xi2 = np.r_[0.1:1.0:100j]
yi2 = c[0]*np.exp(-xi2) + c[1]*xi2
plt.plot(xi,zi,'x',xi2,yi2)
plt.axis([0,1.1,3.0,5.5])
plt.xlabel('$x_i$')
plt.title('Data fits')
plt.show()
# In[70]:
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
# Define a function which calculates the derivative
def dy_dx(y, x):
    return x - y
xs = np.linspace(0,5,100)
y0 = 1.0
ys = odeint(dy_dx, y0, xs)
ys = np.array(ys).flatten()
y_exact = xs - 1 + 2*np.exp(-xs)
y_difference = ys - y_exact
plt.plot(xs, ys, xs, y_exact, "+");
plt.show()
# In[71]:
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
def dU_dx(U, x):
    # Here U is a vector such that y=U[0] and z=U[1]. This function should return [y', z']
    return [U[1], -2*U[1] - 2.*U[0] + 5.*np.cos(2*x)]
U0 = [0, 0]
xs = np.linspace(0, 10, 200)
Us = odeint(dU_dx, U0, xs) # Same as before but instead of N scalars, the input is 2xN
ys = Us[:,0]
plt.plot(xs,ys)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Damped harmonic oscillator");
plt.show()
# In[72]:
import numpy as np
x = np.arange(9).reshape((3,3))
print(x)
main_diagonal=np.diag(x)
print(main_diagonal)
single_positive_offset_diagonal=np.diag(x, k=1)
print(single_positive_offset_diagonal)
single_negative_offset_diagonal=np.diag(x, k=-1)
print(single_negative_offset_diagonal)
# In[73]:
import numpy as np
from numpy import linalg as LA
A=np.array([[0, 1], [1, 0]])
print(A)
w, v = LA.eig(A)
print(w)
print(v)
for i in range(0, 2):
        print(np.dot(A[:,:], v[:,i])- w[i] * v[:,i])
# In[74]:
import numpy as np
import matplotlib.pyplot as plt
# Set maximum iteration
maxIter = 800
# Set Dimension and delta
lenX = lenY = 10 #we set it rectangular
delta = 1
# Boundary condition
Ttop = 100
Tbottom = 50
Tleft = 100
Tright = 100
# Initial guess of interior grid
Tguess = 20
# Set colour interpolation and colour map
colorinterpolation = 50
colourMap = plt.cm.coolwarm 
# Set meshgrid
X, Y = np.meshgrid(np.arange(0, lenX), np.arange(0, lenY))
# Set array size and set the interior value with Tguess
T = np.empty((lenX, lenY))
T.fill(Tguess)
# Set Boundary condition
T[(lenY-1):, :] = Ttop
T[:1, :] = Tbottom
T[:, (lenX-1):] = Tright
T[:, :1] = Tleft
# In[75]:
# Iterate 
for iteration in range(0, maxIter):
    for i in range(1, lenX-1, delta):
        for j in range(1, lenY-1, delta):
            T[i, j] = 0.25 * (T[i+1][j] + T[i-1][j] + T[i][j+1] + T[i][j-1])
# Configure the contour
plt.title("Temperature")
plt.contourf(X, Y, T, colorinterpolation, cmap=colourMap)
# Set Colorbar
plt.colorbar()
# Show the result in the plot window
plt.show()