#!/usr/bin/env python
# coding: utf-8
# In[3]:
import numpy as np
a = np.array([1, 2, 3])  # Create a rank 1 array
print (type(a))           # Prints "<type 'numpy.ndarray'>"
print (a.shape)            # Prints "(3,)"
print (a[0], a[1], a[2])   # Prints "1 2 3"
a[0] = 5                 # Change an element of the array
print (a)                  # Prints "[5, 2, 3]"
# In[4]:
b = np.array([[1,2,3],[4,5,6]])     # Create a rank 2 array
print (b)
print (b.shape)                     # Prints "(2, 3)"
print (b[0, 0], b[0, 1], b[1, 0] )  # Prints "1 2 4"
# In[8]:
c=np.array([[[ 0,  1,  2,  3], [ 4,  5,  6,  7], [ 8,  9, 10, 11]], 
          [[12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]]])
# In[10]:
print(c.shape)
# In[11]:
# Create an array of ones
np.ones((3,4))
# In[12]:
# Create an array of zeros
np.zeros((2,3,4),dtype=np.int16)
# In[15]:
# Create random matrix/arrays
# 1. Return random floats  in the half-open interval [0.0, 1.0), with 2 by 2
print(np.random.random((2,2))) 
print("-"*5)
# 2. Return a sample (or samples) from the “standard normal” distribution.s
# The standard normal distribution is a normal distribution with a mean of 0 and a standard deviation of 1.
print(np.random.randn(5))
print("-"*5)
# 3. Return random integer from low to upper bound with size.
print(np.random.randint(low=0, high=10, size=5))
# In[16]:
# Create an empty array
np.empty((3,2))
# In[17]:
# Create a full array
np.full((2,2),7)
# In[22]:
# Create an array of evenly-spaced values with step size
np.arange(10,25,5)
# In[24]:
# Create an array of evenly-spaced values with number of samples
np.linspace(10,25,5)
# In[25]:
# Create an identity matrices
np.eye(4)
# In[28]:
## make an array, then reshape the size
arr1 = np.arange(8)
arr2 = np.arange(8).reshape(2,4)
print(arr1)
print(" "*5)
print(arr2)
# In[30]:
## display basic info of an array
print ('Data type                :', arr2.dtype)
print ('Total number of elements :', arr2.size)
print ('Number of dimensions     :', arr2.ndim)
print ('Shape (dimensionality)   :', arr2.shape)
print ('Memory used (in bytes)   :', arr2.nbytes)
# In[63]:
######please insert your code here######
# In[64]:
######please insert your code here######
# In[31]:
# type of an array element
zero = np.zeros((1,3), dtype='int32')
print ("zero: ", zero)
print ("object type is: ", type(zero))
print ("Array zero's data type is: ", zero.dtype)
# In[36]:
# short dtype notations
dt1 = np.dtype("int32")
dt2 = np.dtype("i")
dt3 = np.dtype("float32")
dt4 = np.dtype("f")
dt5 = np.dtype("object")
dt6 = np.dtype("O")
# In[40]:
dt5
# In[49]:
import numpy as np
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
print(a)
print()
print(a.shape)
# In[50]:
print (a)  
a[0, 1] = 77    # value at b[0, 1] gets updated from 2 to 77
print (" "*5)
print (a) 
# In[53]:
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
print(a)
print(" ")
# An example of integer array indexing.
# The returned array will have shape (3,) and 
print (a[[0, 1, 2], [0, 2, 0]])  # Prints "[1 7 9]"
print(" ")
# The above example of integer array indexing is equivalent to this:
print (np.array([a[0, 0], a[1, 2], a[2, 0]]))  # Prints "[1 4 5]"
# In[54]:
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
row_r1 = a[1, :]    # Rank 1 view of the second row of a  
row_r2 = a[1:2, :]  # Rank 2 view of the second row of a
print ("Output array: {0}, Output rank: {1}".format(row_r1, row_r1.shape))  # Prints "[5 6 7 8] (4,)"
print ("Output array: {0}, Output rank: {1}".format(row_r2, row_r2.shape))  # Prints "[[5 6 7 8]] (1, 4)"
# In[58]:
import numpy as np
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
bool_idx = (a > 6)  # Find the elements of a that are bigger than 6;
                    # this returns a numpy array of Booleans of the same
                    # shape as a, where each slot of bool_idx tells
                    # whether that element of a is > 6.
            
print (bool_idx)     
# We use boolean array indexing to construct a rank 1 array
# consisting of the elements of a corresponding to the True values
# of bool_idx
print (a[bool_idx]) 
# In[61]:
print (a[a > 6])
# In[1]:
######please insert your code here#######
# In[73]:
######please insert your code here#######
# In[74]:
import numpy as np
x = np.array([[1,2],[3,4]], dtype=np.float64)
y = np.array([[5,6],[7,8]], dtype=np.float64)
# Elementwise sum; both produce the array
print (x + y)
print (np.add(x, y))
print("")
# Elementwise difference; both produce the array
print (x - y)
print (np.subtract(x, y))
print("")
# Elementwise product; both produce the array
print (x * y)
print (np.multiply(x, y))
print("")
# Elementwise division; both produce the array
print (x / y)
print (np.divide(x, y))
print("")
# Elementwise square root; produces the array
print (np.sqrt(x))
# In[84]:
# matrix mulitplication
a = np.random.random((100,100))
b = np.random.random((100,100))
# Method 1: matrix multiplication using universal function
def mult1(a,b):
    return a * b
# Method 2: matrix multiplication using loops -  !!!should always avoid for loops!!
def mult1oop(a,b):
    c = np.empty(a.shape)
    
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            c[i,j] = a[i,j] * b [i,j]
            
    return c
# In[85]:
import numpy as np
import timeit
get_ipython().run_line_magic('timeit', 'mult1(a,b) #Matrix Element-wise Multiply won!!!')
# In[86]:
get_ipython().run_line_magic('timeit', 'mult1oop(a,b)')
# In[89]:
import numpy as np
x = np.array([[1,2],[3,4]])
print (np.sum(x))  # Compute sum of all elements; prints "10"
print (np.sum(x, axis=0))  # Compute sum of each column; prints "[4 6]"
print (np.sum(x, axis=1))  # Compute sum of each row; prints "[3 7]"
# In[93]:
arr = np.arange(8).reshape(2,4)
print(arr)
print("")
print ('Minimum and maximum             : {}, {}'.format(arr.min(), arr.max()))
print ('Sum and product of all elements : {}, {}'.format(arr.sum(), arr.prod()))
print ('Mean and standard deviation     : {}, {}'.format(arr.mean(), arr.std()))
# In[94]:
arr.cumsum()
# In[95]:
print ('For the following array:\n', arr)
print ('The sum of elements along the rows is    :', arr.sum(axis=1))
print ('The sum of elements along the columns is :', arr.sum(axis=0))
# In[96]:
a = np.array([[1, 2], [3, 4]])
print (np.mean(a))
print (np.mean(a, axis=0))  ## average along y-axis
print (np.mean(a, axis=1))  ## average along x-axis
print (a.mean())