"""
This module provides some of the core utilities of  the Scalpel framework. This includes Visitor functions for classes, function definitions and calls, as well as other visitor utilities.
This module also provides an interface for MNode class. A MNode class  is a representation of a Module as a node in a control flow graph (CFG).
It extracts information about the node, such as its id, its statements, function definitions, imports and its exits from the source code. The MNode class is used by the CFGBuilder class to build CFGs from Python ASTs. 
"""