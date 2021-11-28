"""
scalpel.import_graph is data structure for contructing an import graph of a python project. 
An import graph represents the dependency relationship of  module files  in the given project. 
This information can be important to understand the import flow, hierarchy, encapsulation as well as software architecture.
Each node in the import graph datastructure is a module file that can be manipulated to extract statements, function calls.
All the leaf nodes in the import graph can be processed future. 
"""