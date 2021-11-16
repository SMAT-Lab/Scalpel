
## Call Graph
### Overview
`scalpel.pycg` module is a wrapper of `PyCG`[3]. It aims to construct the call graphs for given Python projects. The basic node can be either a function, a class or a module. The edges represents calling relationships between program nodes. Call Graph is an essential component in most static analysis and can be used to build more sophisicated applications.

  
### How to use Call Graph
We use */example_pkg* package as an example and below is the folder structure of it.

```
-example_pkg
    -main.py
    -sub_folder1
        -module1.py
        -module2.py
    -sub_folder2
```
To construct the call graph a python application, import and use `CallGraphGenerator` from `scalple.pycg.pycg`.

```python
from scalpel.pycg.pycg import CallGraphGenerator
cg_generator = CallGraphGenerator(["main.py"], "example_pkg")
cg_generator.analyze()
```
CallGraphGenerator takes two parameter, entry_points and package. package is the root folder of the package that we are generating a call graph for. And entry_points is a list of entry point files of the call graph.
Now the call graph is generated, many useful functions can be utilized to analyze the package. To output all function calls, `output_edges` can be used:

```python
edges = cg_generator.output_edges()
```
And one can use `output_internal_mods` and `output_external_mods` to get all internal/external modules
```python
internal_mods = cg_generator.output_internal_mods
external_mods = cg_generator.output_external_mods
```
To directly operates on the call graph, one can call `output`.
```python
cg = cg_generator.output()
```
`scalpel.pycg` also provides a tool `` to store the call graph results in the JSON format.
```python
from scalpel.pycg import formats
import json 
formatter = formats.Simple(cg)
if args.output:
    with open("example_results.json", "w+") as f:
        f.write(json.dumps(formatter.generate()))
```


\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Call Graph Example](../examples/cg_tutorial.py)


### APIs
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)

### Reference
1. [Call Graph Concepts](https://en.wikipedia.org/wiki/Call_graph)
2. [PyCG: Practical Call Graph Generation in Python. In 43rd International Conference on Software Engineering, 2021](https://vitsalis.com/papers/pycg.pdf). 
3. [The pycg library ](https://pypi.org/project/pycg/)

