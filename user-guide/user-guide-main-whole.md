# Table of contents
- [Introduction](#introduction)
  * [Setting up Scalpel](#setting-up-scalpel)
  * [Roadmap](#roadmap)
- [Core Utilities of Scalpel](#core-utilities-of-scalpel)
  * [Call Graph](#call-graph)
  * [Control Flow Graph](#control-flow-graph)
  * [Rewriter](#rewriter)
  * [Static Single Assignment](#static-single-assignment)
- [Middle Level Modules](#middle-level-modules)
  * [Import Graph](#import-graph)
  * [Import Graph](#import-graph)
- [Application Level Modules](#application-level-modules)


## Introduction
Introduction of Scalpel framework here.

### Setting up Scalpel
Here introduces how to set up and run Scalpel as a dependency.\
...\
...\
...\
...

```python
pip install .
```
...\
...\
...\
...\
...\
...\
...\
...\
...\
...

### Roadmap
Some demonstration of the composition of the library.\
...\
...\
...\
...
![title](https://lucid.app/publicSegments/view/079f413f-8fd5-4c4f-9ad2-1a3cad30583d/image.png)
...\
...\
...\
...\
...\
...\
...\
...\
...

## Core Utilities of Scalpel
The core level modules of Scapel operates on the scope of single procedure (intra-procedural)\

### Call Graph
Introduction to Call Graph module...\
...\
...\
...\
...\

How to use Call Graph
```python
from scalpel.pycg import CallGraphGenerator
entry_points = xxx
package = xxx
cfg = CallGraphGenerator(entry_points,package)
```
...\
...\
...\
...\
...\
...\
...\
...\
...\
...\
...



### Control Flow Graph
Introduction to Control Flow Graph module...\
...\
...\
...\
...\


How to use Control Flow Graph
```python
from scalpel.cfg import CFGBuilder
fun_node = ast.Module(body=new_body)
cfg = CFGBuilder().build(node.name, fun_node)
```
...\
...\
...\
...\
...\
...\
...\
...\
...\
...


### Rewriter
Introduction to Rewriter module...\
How to use Rewriter\
...

### Static Single Assignment
Introduction to Static Single Assignment module...\
How to use Static Single Assignment\
...

## Middle Level Modules
The middle level modules of Scapel operates on the scope of the whole program (inter-procedural)\

### Import Graph
Introduction to Import Graph module...\
How to use Import Graph\
...