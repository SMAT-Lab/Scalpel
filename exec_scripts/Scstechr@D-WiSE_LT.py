#!/usr/bin/env python
# coding: utf-8
# In[1]:
print('Hello World')
# In[2]:
def main():
    print('Hello World')
if __name__ == "__main__":
    main()
# In[3]:
lst = []                     #空の配列
lst = [0, 0, 0]              #要素をカンマで区切って入れる
lst = [0 for i in range(3)]  #range()というイテレータを用いたリスト内包表記 (速い)
lst = list(range(3))         #list()というコンストラクタを用いた初期化 (かなり速い)
# In[4]:
lst = [1, 2, 3, 4]
print(lst)
# In[5]:
lst.append(5)                #末尾に要素を追加. 破壊的メソッド.
print(lst)
# In[6]:
lst.insert(0, 1)             #インデックス(0)を指定して整数(1)を挿入. 
print(lst)
# In[7]:
print(dir(list))
# In[8]:
help(list.append)
# In[9]:
lst = [1, 2, 3]
print(type(lst))
# In[10]:
import numpy as np            #numpyをnpという名前でimportして利用する
# In[11]:
print(dir(np))                #numpyで定義された関数その他を出力
# In[12]:
print(dir(np.ndarray))                 #np.ndarray用に定義された関数その他
# In[13]:
def lst_init(n):
    """ listを用いた実装 """
    lst = list(range(n))
    return lst
    
def array_init(n):
    """ numpyを用いた実装 """
    array = np.arange(n)
    return array
# In[14]:
get_ipython().run_line_magic('timeit', 'lst_init(10000)')
# In[15]:
get_ipython().run_line_magic('timeit', 'array_init(10000)')
# In[16]:
np.sum(np.array([1,2,3,4]))
# In[17]:
get_ipython().run_line_magic('timeit', 'sum(lst_init(10000))')
# In[18]:
get_ipython().run_line_magic('timeit', 'np.sum(array_init(10000))')
# In[19]:
array = np.array([1, 2, 3, 4])      #listをnp.array()に代入する
print(array)
# In[20]:
array = np.arange(1,5)              #等差行列を返すnp.arange()を使う
print(array)
# In[21]:
array = np.zeros(4)                 #要素が全て0の行列
print(array)
# In[22]:
array = np.ones(4)                 #要素が全て1の行列
print(array)
# In[23]:
array = np.array([[1,2],[3,4]])         #listを中身にもつlistをnp.array()に代入
print(array)
# In[24]:
array = np.arange(1,5).reshape(2,2)     #reshape()で変形
print(array)
# In[25]:
array = np.zeros([2,2])                 #np.zeros()にlistを入れると多次元に
print(array)
# In[26]:
array = np.ones([2,3])                 #np.ones()にlistを入れると多次元に
print(array)
# In[27]:
array = np.identity(3)                 #np.identityは単位行列
print(array)
# In[28]:
a = np.array([1,2,3])
b = np.array([4,5,6])
# In[29]:
a+b
# In[30]:
a-b
# In[31]:
a*b
# In[32]:
a/b
# In[33]:
print(dir(np.linalg))
# In[34]:
c = np.arange(1,5).reshape(2,2)
print(c)
# In[35]:
np.linalg.det(c)                 #行列式
# In[36]:
np.linalg.norm(c)                #ノルム
# In[37]:
np.linalg.inv(c)                 #逆行列
# In[38]:
np.linalg.svd(c)                 #特異値分解
# In[39]:
print(dir(np.random))
# In[40]:
import matplotlib.pyplot as plt
# In[41]:
R = np.random.rand(10000)
plt.hist(R, bins=1000)
plt.show()
# In[42]:
R = np.random.randn(10000)
plt.hist(R, bins=1000)
plt.show()
# In[43]:
R = np.random.poisson(lam=10, size=10000)
plt.hist(R, bins=100)
plt.show()
# In[44]:
array = np.arange(9)
pmf = np.array([0,0,0.5,0.28,0,0,0,0,0.22])
R = np.random.choice(array, size = 10000, p=pmf)
plt.hist(R, bins=100)
plt.show()
# In[45]:
print(dir(np.poly1d))
# In[46]:
f = np.poly1d([2, 3, 4, 5])
print(f)
# In[47]:
f(0)
# In[48]:
f = f.deriv()
print(f)
# In[49]:
import scipy                            #numpyと違い略式を用いないのが一般的
# In[50]:
print(dir(scipy))                       #numpyに勝るとも劣らないライブラリ群
# In[51]:
help(scipy.zeros)
# In[52]:
type(scipy.zeros(10))                        #得られるはnp.ndarray
# In[53]:
from scipy.sparse import lil_matrix
#疎行列を宣言
a = lil_matrix((4,4))
#非ゼロ要素を代入
a[0,0] = 1
a[0,1] = 2
# In[54]:
import sympy
# In[55]:
print(dir(sympy))
# In[56]:
a = sympy.Rational(1/2)              #分数型
print(a)
# In[57]:
x = sympy.Symbol('x')                  #変数ではなくSymbolとして利用
y = sympy.Symbol('y')
# In[58]:
f = (x+y)**2                           #多項式の定義
print(f)
# In[59]:
f = sympy.expand(f)                    #多項式の展開
print(f)
# In[60]:
A = sympy.Matrix([[1,x], [y,1]])       #Symbolを含んだ行列を定義
print(A)