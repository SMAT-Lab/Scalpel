"""
The control-flow graph(CFG) is an essential component in static flow analysis with applications such as program
optimization and taint analysis.
scalpel.cfg module is used to construct the control flow graph for given python programs. The basic unit in the CFG,
Block, contains a list of sequential statements that can be executed in a program without any control jumps. The Blocks
are linked by Link objects, which represent control flow jumps between two blocks and contain the jump conditions in
the form of an expression. Please see the example diagram a control flow graph ![Fibonacci CFG](https://raw.githubusercontent.com/SMAT-Lab/Scalpel/dev/resources/cfg_example.png)
"""
from .builder import CFGBuilder
from .model import Block, Link, CFG
