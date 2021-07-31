#!/usr/bin/env python
# coding: utf-8
# In[2]:
import matplotlib.pyplot as plt
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  
#这个explode是指将饼状图的部分与其他分割的大小，这里之分割出hogs，度数为0.1，这个数字表示和主图分割的距离
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  
#这个equal是让整个饼图为一个圆形，如果不加，则是椭圆形
plt.show()
# In[8]:
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
# vc=[1,2,39,0,8]
# vb=[1,2,38,0,8]
# image = np.corrcoef(vc, vb)
np.random.seed(0)
image = np.random.uniform(size=(6, 6))
# print (image)
ax.imshow(image, cmap=plt.cm.gray, interpolation='nearest',origin='upper')
ax.set_title('dropped spines')
# Move left and bottom spines outward by 10 points
ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_position(('outward', 10))
# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
plt.show()
#image是一个6*6的矩阵，此类型的图可以显示矩阵数字的大小，颜色越浅，说明这个位置的数组越大
#举个栗子
print(image[2][1])
print(image[2][2])
#是不是很神奇 [滑稽]
# In[90]:
import pandas as pd
from numpy import mean, multiply, cov, corrcoef, std
df = pd.read_csv('matplotlib3.csv')
df.rename(columns={'Unnamed: 0':'date'},inplace=True)
df.head()
# In[20]:
b=[1,3,5,6]
print (np.cov(b))
print (sum((np.multiply(b,b))-np.mean(b)*np.mean(b))/3)
# In[25]:
vc=[1,2,39,0,8]
vb=[1,2,38,0,8]
print (mean(multiply((vc-mean(vc)),(vb-mean(vb))))/(std(vb)*std(vc)))
#corrcoef得到相关系数矩阵（向量的相似程度）
print (corrcoef(vc,vb))
# In[87]:
l = []
for x in df.columns[1:]:
    l.append(df[x].values)
matrix = np.mat(l)
image = corrcoef(matrix)
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(image, cmap=plt.cm.gray, interpolation='nearest',origin='lowwer')
get_ipython().run_line_magic('pinfo', 'ax.imshow')
ax.set_title('dropped spines')
# Move left and bottom spines outward by 10 points
ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_position(('outward', 10))
# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
plt.xticks([0, 1, 2, 3, 4, 5],df.columns[1:])
plt.yticks([0, 1, 2, 3, 4, 5],df.columns[1:])
plt.show()
# In[114]:
fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(df.index, df['601398.XSHG'], label='601398.XSHG')
plt.plot(df.index, df['601939.XSHG'], label='601939.XSHG')
plt.plot(df.index, df['601939.XSHG']-df['601398.XSHG'], label='dif')
plt.legend(loc='upper left')
ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_position(('outward', 10))
plt.show()