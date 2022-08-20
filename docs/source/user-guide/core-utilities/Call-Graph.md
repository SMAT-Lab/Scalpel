# Call Graph

## Overview
A call graph depicts calling relationships between subroutines in a computer program. It is an essential component in most static analysis and can be leveraged to build more sophisicated applications such as profiling, vunerability propagation and refactoring.
`scalpel.call_graph.pycg` module is a wrapper of `PyCG`[3]. It aims to construct the call graphs for given Python projects. The basic node can be either a function, a class or a module. The edges represent calling relationships between program nodes. 

  
## How to use Call Graph
We use */example_pkg* package as an example and below is the folder structure of it.

```
-example_pkg
    -main.py
    -sub_folder1
        -module1.py
        -module2.py
    -sub_folder2
```
To construct the call graph of a python application, import and use `CallGraphGenerator` from `scalpel.call_graph.pycg`.

```python
from scalpel.call_graph.pycg import CallGraphGenerator
cg_generator = CallGraphGenerator(["main.py"], "example_pkg")
cg_generator.analyze()
```
CallGraphGenerator takes two parameters, entry_points and package. package is the root folder of the package that we are generating a call graph for. And entry_points is a list of entry point files of the call graph.
Now the call graph is generated, many useful functions can be utilized to analyze the package. To output all function calls, `output_edges` can be used:

```python
edges = cg_generator.output_edges()
```
And one can use `output_internal_mods` and `output_external_mods` to get all internal/external modules.
```python
internal_mods = cg_generator.output_internal_mods
external_mods = cg_generator.output_external_mods
```
To directly operates on the call graph, one can call `output`.
```python
cg = cg_generator.output()
```
`scalpel.call_graph.pycg` also provides a tool `formats.Simple()` to store the call graph results in the JSON format.For more functions, please refer to [PyCG](https://pypi.org/project/pycg/).
```python
from scalpel.call_graph.pycg import formats
import json 
formatter = formats.Simple(cg)
with open("example_results.json", "w+") as f:
    f.write(json.dumps(formatter.generate()))
```


\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Call Graph Example](../examples/cg_tutorial.py)


## APIs
Please refer to the API documentation: {any}`scalpel.call_graph`


## Reference
1. [Call Graph Concepts](https://en.wikipedia.org/wiki/Call_graph)
2. [PyCG: Practical Call Graph Generation in Python. In 43rd International Conference on Software Engineering, 2021](https://vitsalis.com/papers/pycg.pdf). 
3. [The pycg library ](https://pypi.org/project/pycg/)
4. [pyan3](https://pypi.org/project/pyan3/)
5. [Code2graph: Automatic generation
of static call graphs for Python source code](https://ieeexplore.ieee.org/document/9000043)


