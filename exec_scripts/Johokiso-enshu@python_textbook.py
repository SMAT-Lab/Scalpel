#!/usr/bin/env python
# coding: utf-8
# In[1]:
# 文字列を複数格納したリスト
words = ['cat', 'window', 'defenestrate']
# In[2]:
for w in words:
    print(w, len(w))
# In[3]:
for i in range(5):
    print(i)
# In[4]:
# 以下の2つのベクトルの内積を計算する。
x = [1.0, 2.0]
y = [1.0, 3.0]
# In[5]:
dot = 0.0
for i in range(len(x)):
    dot += x[i] * y[i]
# In[6]:
print(dot)
# In[7]:
# 解答をここに記入する
# In[8]:
A = [[1.0, 0.0], [2.0, 3.0]]
print(A)
# In[9]:
print(A[0])
# In[10]:
print(A[0][1])
# In[11]:
# 解答をここに記入する
# In[12]:
len(x) # リスト（など）を引数にとり、要素数を返す関数
# In[13]:
# 関数の例 `def` + 関数の名前（この場合はlist_dot）+ カッコ　として定義する。
# カッコの中に引数を入れる。
def list_dot(x1, x2):
    """
    2つのリストを受け取り、その内積を計算する関数。
    なお関数に関する説明は、
    このように３つの連続するダブルコーテーション内に記述することが推奨されている。
    """
    dot = 0.0
    for i in range(len(x1)):
        dot += x1[i]*x2[i] # x += y は、x に x+y を代入することを表す。
    return dot # return 文で計算した値を返す。
# In[14]:
x = [1.0, 2.0]
y = [2.0, 1.0]
print(list_dot(x, y))
# In[15]:
x = [1.0, -2.0]
y = [2.0, 1.0]
print(list_dot(x, y))
# In[16]:
# 解答をここに記入する
# In[17]:
# まず最初に、グラフ描画ライブラリと、数値計算ライブラリをimportしておく。
import numpy as np
# 同様にmatplotlibもimportしておく。
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# In[18]:
# sin 関数
np.sin(1)
# In[19]:
# まず、計算する範囲、個数を指定する。今回は、-5~5, 100 点で計算する。
x = []
y = []
for i in range(100):
    x.append(-5.0 + 10.0 / 100 * i)
    y.append(np.sin(x[i]))
# In[20]:
plt.plot(x, y, '-o')
# In[21]:
# 解答をここに記入する
# In[22]:
# 解答をここに記入する
# In[23]:
# 解答をここに記入する
# In[24]:
def discriminant(a, b, c):
    """
    a x**2 + b x + c = 0 に実数解が存在するか調べるプログラム。
    ２つの実数解が存在する場合は `two real roots` を、重根が存在する場合は `one real root`を、
    実数解が存在しない場合は `two complex roots` を表示する。
    """
    d = b**2 - 4.0*a*c
    if d > 0.0:
        print('two real roots')
    elif d == 0.0:
        print('one real root')
    else:
        print('two complex roots')
# In[25]:
discriminant(3.0, 2.0, 1.0)
# In[26]:
# 2+3i は以下のように表す。
np.complex(2.0,3.0)
# In[27]:
# 解答をここに記入する
# In[28]:
# 解答をここに記入する
# In[29]:
# scipy.special  をインポート
import scipy.special
# In[30]:
# まず、計算する範囲、個数を指定する。今回は、-5~5, 100 点で計算する。
x = []
j0 = [] # α=0 のベッセル関数を計算し格納するリスト
j1 = [] # α=1
j2 = [] # α=2
for i in range(100):
    x.append(20.0 / 100 * i)
    j0.append(scipy.special.jv(0, x[i])) 
    j1.append(scipy.special.jv(1, x[i])) 
    j2.append(scipy.special.jv(2, x[i]))
# In[31]:
# これらの結果をプロットする
plt.plot(x, j0, label='a=0') # `label=` のあとに文字列を指定することにより、後ほど凡例を表示できる。
plt.plot(x, j1, label='a=1')
plt.plot(x, j2, label='a=2')
plt.legend() # 凡例を表示するためのコマンド
# In[32]:
# 解答をここに記入する