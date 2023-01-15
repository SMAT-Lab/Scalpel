
# Scalpel: The Python Static Analysis Framework

[![Documentation Status](https://readthedocs.org/projects/python-scalpel/badge/?version=latest)](https://python-scalpel.readthedocs.io/en/latest/?badge=latest)

Scalpel is a Python Static Analysis Framework. It provides essential program analysis functions for facilitating the implementation of client applications focusing on statically resolving dedicated problems.

<img src="https://github.com/SMAT-Lab/Scalpel/blob/main/docs/source/_static/resources/Scalpel.svg" width="550">

# Contributing

We will be highly appreciated it if you can contribute to this project. Please feel free to do so by [submiting issue reports](https://github.com/SMAT-Lab/Scalpel/issues) or directly [adding pull requests](https://github.com/SMAT-Lab/Scalpel/pulls). We hope to obtain help for:
1. New features. If you believe your publication/open-source project can be part of our framework, please contact us.
2. Bug reports. 
3. Documentation. 
4. Code refactoring 

## Setting up Scalpel
Clone the repository of Scalpel and in the root directory simply run:
```python
python -m pip install .
```

## Brief Introduction

Detailed user guides can be found at [python-scalpel.readthedocs.io](http://python-scalpel.readthedocs.io/).

We aim to provide Scalpel as a generic Python static analysis framework that includes as many functions as possible (e.g., to easily build inter-function control-flow graph, to interpret the import relationship of different Python modules, etc.) towards facilitating developers to implement their dedicated problem-focused static analyzers. The following figure depicts the current architecture of its design.

![Scalpel Design](/docs/source/_static/resources//scalpel_design.png)

* Function 1: Code Rewriter. The code rewriter module is designed as a fundamental function for supporting systematic changes of existing Python programs. Two preliminary usages of this function are to (1) simplify the programs for better static analysis and (2) optimize or repair problematic programs. For supporting the first usage, we integrate into the framework a database including a set of rules indicating how matched code snippets should be transformed. This database should be continuously extended to fulfill the complicated simplification requirements for achieving effective static analysis of Python programs. For supporting the second usage, inspired by the optimization mechanism provided by Soot (one of the most famous static Java program analysis frameworks), we also set up a transformation process with dedicated callback methods to be rewritten by users to optimize Python code based on their customized needs.

* Function 2: Control-Flow Graph Construction. The control-flow graph(CFG) construction module generates intra-procedural CFGs, which are an essential component in static flow analysis with applications such as program optimization and taint analysis. A CFG represents all paths that might be traversed through a program during its execution. The CFGs of a Python project can be combined with the call graph to generate an inter-procedural CFG of the project.

* Function 3: Static Single Assignment (SSA) Representation. The static single assignment module provides compiler-level intermediate representations (IR) for code analysis. It can not only be used for symbolic execution, but also for constant propagation. By renaming each variable assignment with different names,  we are able to obtain explicit use-def chains, therefore precisely tracking how data flow in the program. 

* Function 4: Alias Analysis. Since variables can point to the same memory location or identical values, the alias analysis function is designed to model such usages. This function can be vital to sound constant propagation. In addition, alias analysis will also benefit type checking as well as API name qualifying. 

* Function 5: Constant Propagation. The constant propagation module will evaluate the actual values for variables at certain program points in different execution paths before runtime. With the actual values known beforehand, we are able to optimize code and detect bugs.  The constant propagation will utilize the representation from the SSA module to keep recording values from each assignment for a single variable. 

* Function 6: Import Graph Construction. In python,  import flows and relations have been pointed out to be important for API mapping, dependency analysis. Our import graph construction aims to provide a data structure to represent these import relationships across the Python module files in the same project. The import graphs of multiple Python projects can be combined to perform inter-library dataflow analysis.

* Function 7: Fully Qualified Name Inferrer. Python APIs or function names can be invoked in different ways depending on how they are imported. However, this results in inconveniences to API usage analysis. In this module, we will convert all function call names to their fully-qualified names which are dotted strings that can represent the path from the top-level module down to the object itself. Various tasks can be benefited from this functionality such as understanding deprecated API  usage, dependency parsing as well as building sound call graphs. 

* Function 8: Call Graph Construction. A call graph depicts calling relationships between methods in a software program. It is a fundamental component in static flow analysis and can be leveraged in tasks such as profiling, vulnerability propagation, and refactoring. This module addresses the challenges brought by complicated features adopted in Python, such as higher-order functions and nested function definitions, to construct the precise call graphs for given Python projects.

* Function 9: Type Inference. Python, as a dynamically typed language, faces the problem of being hard to utilize the full power of traditional static analysis. This module infers the type information of all variables including function return values and function parameters in a Python program, making more sophisticated static analysis possible for Python. We utilize backward data-flow analysis and a set of heuristic rules to achieve high precision.

## API Documentation

The Scalpel's API documentation is available at [python-scalpel.readthedocs.io](http://python-scalpel.readthedocs.io/en/latest/api/).

<br />
<p>We release Scalpel source code in the hope of benefiting others. You are kindly asked to acknowledge usage of the tool by citing the following article: </p>

```
@article{li2022scalpel, 
title={Scalpel: The Python Static Analysis Framework}, 
author={Li, Li and Wang, Jiawei and Quan, Haowei}, 
journal={arXiv preprint arXiv:2202.11840}, 
year={2022} 
}
```

Scalpel is invited to be presented at EuroPython 2022. EuroPython is the oldest and longest running volunteer-led Python programming conference on the planet!


<img src="https://github.com/SMAT-Lab/Scalpel/blob/main/docs/source/_static/resources//europython.png" width="400">



## Acknowledgement
This project has been inspired and supported by many existing works. If you think your work appears in this project but has not been mentioned yet, please let us know by any means.

1. [Fuzzyingbook](https://www.fuzzingbook.org/) by Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler.
2. [Debugging book](https://www.debuggingbook.org/) by Andreas Zeller.
3. [StaticCFG](https://github.com/coetaur0/staticfg).
4. [PyCG: Practical Call Graph Generation in Python](https://vitsalis.com/papers/pycg.pdf), ICSE 2021. 
5. [A Simple, Fast Dominance Algorithm](https://www.cs.rice.edu/~keith/EMBED/dom.pdf) Keith D. Cooper, Timothy J. Harvey, and Ken Kennedy
6. [COS598C Advanced Compilers](https://www.cs.princeton.edu/courses/archive/spr04/cos598C/lectures/02-ControlFlow.pdf), Princeton University
7. [Restoring Execution Environments of Jupyter Notebooks](https://arxiv.org/ftp/arxiv/papers/2103/2103.02959.pdf)
8. [Static Single Assignment Book](https://compilers.cs.uni-saarland.de/papers/bbhlmz13cc.pdf)

