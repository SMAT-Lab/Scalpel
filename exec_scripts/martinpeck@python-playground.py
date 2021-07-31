#!/usr/bin/env python
# coding: utf-8
# In[16]:
from itertools import cycle
# set up a cycle that flips between B (Black) and W (White)
colours = cycle(["B", "W"])
for row in range(8):
    for col in range(8):
        colour = next(colours)                
        print(colour, end="")
    print("")
        
    
# In[36]:
from itertools import cycle
   
servers = ['192.168.0.1', '192.168.0.2', '192.168.0.3', '192.168.0.4']
server_ring = cycle(servers)
       
for _ in range(10):
    print(next(server_ring))