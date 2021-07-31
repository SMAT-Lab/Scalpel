#!/usr/bin/env python
# coding: utf-8
# In[1]:
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
# In[2]:
testcase = np.matrix([
    [0, 1, 1],
    [0, 2, 3],
    [0, 4, 4],
    [0, 5, 3],
    [1, 3, 1],
    [2, 3, 2],
    [4, 5, 1]
])
# In[11]:
tree = nx.Graph()
G = nx.Graph()
graph = np.array(testcase)
graph = tuple(map(tuple, graph))
G.add_weighted_edges_from(graph)
# Start with the first node in the graph
tree.add_node(G.nodes()[0])
# In[4]:
print(graph)
# In[12]:
# Find the minimum weight edge connected to the nodes in the new graph
edges = 0
while (edges < len(G.nodes()) - 1):
    minweight = 999999999
    minedge = (-1, -1)
    for node in tree.nodes():
        for neighbor in G.neighbors(node):
            if G.get_edge_data(node, neighbor)['weight'] < minweight:
                if (neighbor in tree.nodes()) == False:
                    minweight = G.get_edge_data(node, neighbor)['weight']
                    minedge = (node, neighbor, minweight)
    # Add the edge to the new graph
    tree.add_weighted_edges_from([minedge])
    edges = edges + 1
# In[15]:
tree.nodes()
tree.edges()