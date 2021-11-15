
## Control Flow Graph
`scalpel.cfg` module is used to construct the CFG of a piece of python program. The basic unit of the CFG, `Block`, contains a list of statements executed in a program without any control jumps. The `Block`s are linked by `Links`, which represents a control flow jump between two blocks and contains the jump condition in the form of an expression. The two components maks up a CFG.



### How to use Control Flow Graph
Below is the demo input python program we will be using. The piece of code generates the Fibonacci sequence and is named "example.py".
```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib_gen = fib()
for _ in range(10):
    next(fib_gen)
```
To build the cfg of a python file, simply import `CFGBuilder` in `scalpel.cfg` and use `build_from_file(name, file_path)`. Other functions can also be used to build a cfg from an python AST tree or a source string.

```python
from scalpel.cfg import CFGBuilder

cfg = CFGBuilder().build_from_file('example.py', './example.py')

```
This returns the CFG for the code in *./example.py* in the cfg variable. This built CFG can be visulized with `build_visual`:
```python
cfg.build_visual('pdf')
```
Below is the produced *exampleCFG.pdf*.
![Fibonacci CFG](../resources/cfg_example.png)
Apart from generating the visual graph, the CFG can be use for many other static analysis purpose.
For example, `get_calls` can be used to get all function calls in each block.
```python
for block in cfg:
    calls = block.get_calls()
```
`backward` can be used to find a variable's value, if not found in the current block, by backtracing in the CFG.
```python
example_block = cfg.get_all_blocks()[-1]
a_value = cfg.backward(example_block,'a',[],[])
```
One can also combined call graph and CFG to construct interprecedual CFG.
\
The tutorial code can be found here:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Control Flow Graph Example](../examples/cfg_tutorial.py)

### APIs
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)\
[Place Holder](placeholder.com)

### Reference
1. [StaticCFG](https://github.com/coetaur0/staticfg).
2. 