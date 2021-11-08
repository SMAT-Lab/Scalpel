
## Control Flow Graph
Introduction to Control Flow Graph module...\
\
\
\
\
\
\


### How to use Control Flow Graph
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
First we construct the CFG by simply calling Builder with the desired entry points and package...
\
```python
from scalpel.pycg import CallGraphGenerator
entry_points = xxx
package = xxx
cfg = CallGraphGenerator(entry_points,package)
```
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
...\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Control Flow Graph Example](example.com)

### APIs
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)

### Reference
1. 
2. 
