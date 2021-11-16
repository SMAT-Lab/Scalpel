
## Import Graph
`scalpel.import_graph` is a module for contructing an import graph of a python project. An import graph represents the dependency relationship of the modules in the project. Each node is a module and each edge represents a one-way import relationship.

### How to use Import Graph
Given three example python modules in */example root folder*, namely */example/module_a.py*, */example/module_b.py*, */example/module_c.py*.
*/example/module_a.py*
```python
from .module_b import B
from .module_c import C

class A:
    def foo(self):
        return
```
*/example/module_b.py*
```python
from .module_c import C

class B:
    def foo(self):
        return
```
*/example/module_c.py*
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
import_graph.build_dir_tree(root_node)
module_dict = import_graph.parse_import(root_node)

```
The returned value is a dictionary where keys are the module names and values are the modules they have imported.
\
\
Example output here.
\
\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Import Graph Example](../examples/import_graph_tutorial.py)

### APIs
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)

### Reference
1. 
2. 
