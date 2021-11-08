
## Call Graph
### Overview
Call Graph is a graph that represents calling relationships between program nodes. It is an essential component in most static analysis. Scalpel provides Call Graph as a cornerstone for users to build more sophisicated static analysis applications...
The basic node in the call graph is...
\
\
\
\
\
  
### How to use Call Graph
The demo input python program we will be using is as follows.
```python
def func(a:int, b:int)->str:
    if True:
        a = str(a)
    else:
        a = 10
    return a

res = func(10,20)
```
First we construct the call graph by simply calling CallGraphGenerator with the desired entry points and package...
\
```python
from scalpel.pycg import CallGraphGenerator
entry_points = xxx
package = xxx
cfg = CallGraphGenerator(entry_points,package)
```
We then can extract all caller of function A ...
\
\
\
...\
...\
...\
...\
...\
...\
...\
...\
...\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Call Graph Example](example.com)


### APIs
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)

### Reference
1. [Call Graph Concepts](https://en.wikipedia.org/wiki/Call_graph)
2. [PyCG: Practical Call Graph Generation in Python. In 43rd International Conference on Software Engineering, 2021](https://vitsalis.com/papers/pycg.pdf). 

