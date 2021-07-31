#!/usr/bin/env python
# coding: utf-8
# In[1]:
set1={"pop", "rock", "soul", "hard rock", "rock", "R&B", "rock", "disco"}
set1
# In[2]:
album_list =[ "Michael Jackson", "Thriller", 1982, "00:42:19",               "Pop, Rock, R&B", 46.0, 65, "30-Nov-82", None, 10.0]
album_set = set(album_list)             
album_set
# In[3]:
music_genres = set(["pop", "pop", "rock", "folk rock", "hard rock", "soul",                     "progressive rock", "soft rock", "R&B", "disco"])
music_genres
# In[5]:
a_set = set(['rap','house','electronic music','rap'])
a_set
# In[8]:
A=[1,2,2,1]
B=set([1,2,2,1])
print(sum(A))
print(sum(B))
# In[9]:
A = set(["Thriller","Back in Black", "AC/DC"] )
A
# In[10]:
A.add("NSYNC")
A
# In[11]:
A.add("NSYNC")
A
# In[12]:
A.remove("NSYNC")
A
# In[15]:
"NSYNC"  in A
# In[16]:
album_set1 = set(["Thriller",'AC/DC', 'Back in Black'] )
album_set2 = set([ "AC/DC","Back in Black", "The Dark Side of the Moon"] )
# In[17]:
album_set1, album_set2
# In[18]:
album_set_3=album_set1 & album_set2
album_set_3
# In[19]:
album_set1.difference(album_set2)  
# In[20]:
album_set2.difference(album_set1)  
# In[21]:
album_set1.intersection(album_set2)   
# In[22]:
album_set1.union(album_set2)
# In[23]:
set(album_set1).issuperset(album_set2)   
# In[24]:
set(album_set2).issubset(album_set1)     
# In[25]:
set({"Back in Black", "AC/DC"}).issubset(album_set1) 
# In[26]:
album_set1.issuperset({"Back in Black", "AC/DC"})   
# In[28]:
album_set3 = album_set1.union(album_set2)
album_set3
# In[34]:
album_set3.issuperset({1, 2})