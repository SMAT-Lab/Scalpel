
# Welcome to Scalpel's documentation!

Scalpel is a Python Static Analysis Framework. It provides essential program analysis functions for facilitating the implementation of client applications focusing on statically resolving dedicated problems. Scalpel includes several fundamental static analysis functions, such as Call graph construction, Control-flow graph construction, Alias analysis, and type Inference.
These functions can be reused by developers to implement client applications that focus on statically resolving dedicated Python problems, such as Detecting bugs, Fixing vulnerabilities, Profiling code and Refactoring code.
Scalpel is a powerful tool that can help developers to improve the quality of their Python code. It is still under development, but it has the potential to become a valuable resource for the Python community. 
<img src="https://github.com/SMAT-Lab/Scalpel/blob/main/docs/source/_static/resources/Scalpel.svg" width="550">

# Current Capabilities
Even though Scalpel is in a development phase, it provides a wide range of fundamental static analysis techniques in Python, including : 
- Call Graph Construction
- Control-Flow Graph Construction
- Type Inference
- Import Graph Construction
- Code Rewriting
- Static Single Assignment (SSA)

These fundamental functions can be applied to various static analysis applications including:
- API Name Qualifying
- Bug and Vulnerability Detection
- Data Flow Analysis
- Taint Analysis


# Future Directions
As Scalpel is in the early development stage, it is rapidly growing and aims to extend its scope for static analysis in Python, which has already been developed for other Programming Languages such as :
- Flow-Sensitive Call Graph Construction
- Fully Qualified Name Inference
- Assignment Graph


# Setting up Scalpel

You can download the source code of Scalpel to install manually or use `pip` to install automatically.
The framework has not been uploaded to PyPI repository yet since it's still in beta.

```python
pip install python-scalpel
```


# Contributing
We will highly appreciate it if you can contribute to this project. Please feel free to do so by [submitting issue reports](https://github.com/SMAT-Lab/Scalpel/issues) or directly [adding pull requests](https://github.com/SMAT-Lab/Scalpel/pulls). We hope to obtain help for:
1. New features. If you believe your publication/open-source project can be part of our framework, please contact us.
2. Bug reports.
3. Documentation.
4. Code refactoring

# Roadmap

```{toctree}
---
maxdepth: 2
caption: Contents
---
user-guide/index
api/index
```

As a general-purpose framework, Scalpel is a layered structure designed to support tasks at different granularity. You can know more from this user guide about different modules.
![title](https://lucid.app/publicSegments/view/079f413f-8fd5-4c4f-9ad2-1a3cad30583d/image.png)


# Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`


# Development Team
Scalpel Framework was first introduced by Li Li,  Jiawei Wang, and  Haowei Quan in the paper [Scalpel: The Python Static Analysis Framework](https://arxiv.org/abs/2202.11840). Scalpel is maintained by the SMAT Lab (SMart Software Analysis and Trustworthy Computing Lab) which is part of the Software Engineering group at Monash University, Australia. Scalpel also receives huge support from the Python community.

# Acknowledgement

This project has been inspired and supported by many existing works. Some implementation of functionalities is taken from published work. If you think your work appears in this project but is not mentioned yet, please let us know by any means. 

1. [Fuzzyingbook](https://www.fuzzingbook.org/).

2. [Debugging book](https://www.debuggingbook.org/).

3. [StaticCFG](https://github.com/coetaur0/staticfg).

4. [PyCG: Practical Call Graph Generation in Python. In 43rd International Conference on Software Engineering, 2021](https://vitsalis.com/papers/pycg.pdf). 
5. [A Simple, Fast Dominance Algorithm](https://www.cs.rice.edu/~keith/EMBED/dom.pdf) Keith D. Cooper, Timothy J. Harvey, and Ken Kennedy
6. [COS598C Advanced Compilers](https://www.cs.princeton.edu/courses/archive/spr04/cos598C/lectures/02-ControlFlow.pdf), Princeton University
7. [Restoring Execution Environments of Jupyter Notebooks](https://arxiv.org/ftp/arxiv/papers/2103/2103.02959.pdf)
8. [Static Single Assignment Book](https://compilers.cs.uni-saarland.de/papers/bbhlmz13cc.pdf)

