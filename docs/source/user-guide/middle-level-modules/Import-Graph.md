# Import Graph

`scalpel.`import_graph` creates a data structure for describing import relationships of a Python project. 
An import graph represents the dependency relationship of module files in the given project. 
This information can be important to understand the import flow, hierarchy, encapsulation as well as software architecture.
Each node in the import graph data structure is a module file that can be manipulated to extract statements and function calls.

All the leaf nodes in the import graph can be processed future. In Python, import flows and relations have been pointed out to be important for API mapping, and dependency analysis. Our import graph construction aims to provide a data structure to represent these import relationships across the Python module files in the same project. The import graphs of multiple Python projects can be combined to perform inter-library dataflow analysis.

## How to use Import Graph

Given three example Python modules in the following example folder where three Python module files are defined. 

```
|-- example
       |-- module_a.py
       |-- module_b.py
       |-- module_c.py

```

```python
#/example/module_b.py
from .module_b import B
from .module_c import C

class A:
    def foo(self):
        return
```

```python
#/example/module_c.py
from .module_c import C

class B:
    def foo(self):
        return
```

```python
import os

class C:
    def foo(self):
        return
```
To build the import graph of the package, import and use `Tree` and `ImportGraph` in `scalpel.import_graph.import_graph`. 

```python
from scalpel.import_graph.import_graph import Tree,ImportGraph

root_node = Tree("import_graph_example_pkg")
import_graph = ImportGraph()
import_graph.build_dir_tree()
module_dict = import_graph.parse_import(root_node)
leaf_nodes = import_graph.get_leaf_nodes()
print(len(leaf_nodes))

```
For each of leaf notes, we can future to extract its type information, function definition list or more meta information. 

The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Import Graph Example](../examples/import_graph_tutorial.py)

## APIs

Please refer to the API documentation: {py:mod}`scalpel.import_graph`



## Reference

