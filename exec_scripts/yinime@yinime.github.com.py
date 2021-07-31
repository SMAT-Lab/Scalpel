#!/usr/bin/env python
# coding: utf-8
# In[1]:
import random
print("Eine Zufallszahl r =", random.random())
# In[10]:
print("Eine Floge von Zufallszahlen ist")
for i in range(10):
    print(random.random())
# In[4]:
print("Falls 'seed' festgesetzt worden ist, wird die erste Zufallszahl wegen der Algorithmen des bestimmten Generators festgestellt.")
random.seed(100)
random.random()
# In[5]:
random.seed(100)
random.random()
# In[6]:
random.random()
# In[8]:
import random
import matplotlib.pyplot as plt
def randSeq(length=500,s=12345):
   random.seed(s)
   return [random.random() for i in range(length)]
def test(n=500, l=5):
   rSeq = randSeq(length = n)
   points = zip(rSeq[0::2],rSeq[l::2])
   plt.figure(figsize=(20,10))
   plt.subplot(2,1,1)
   plt.title("A Random Sequence")
   plt.plot(rSeq)
   plt.subplot(2,1,2)
   plt.title("Scatter Plot")
   plt.scatter(*zip(*points))
   plt.tight_layout()
   plt.show()
test()