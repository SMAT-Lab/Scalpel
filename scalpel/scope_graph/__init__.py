"""
In this sub-module, we implement the scope graph for Python programs. 
The overall idea is borrowed from the scope graph theory, please see references.
For name binding and resolution, we follow the Local, Enclosing, Global and Built-in(LEGB) rule instead of the resolution calculus in the scope graph theory.


A scope is an abstraction over a group of nodes in the abstract syntax tree
that behave uniformly with respect to name resolution.

Each program has a scope graph G, whose nodes are a finite set of scopes S(G).

Every program has at least one scope, the global or root scope.

Each scope S has an associated finite set D(S) of declarations and finite set R(S) of references (at particular
program positions), and each declaration and reference in a program belongs to a unique scope.

A scope is the atomic grouping for name resolution:
- each reference x_i^R in a scope resolves to a declaration of the same variable x_j^D in the scope, if one exists.

Intuitively, a single scope corresponds to a group of mutually recursive definitions, e.g., a letrec block, the declarations

in a module, or the set of top-level bindings in a program.


[References]

1. Neron, P., Tolmach, A., Visser, E., Wachsmuth, G. (2015). A Theory of Name Resolution. In: Vitek, J. (eds) Programming Languages and Systems.
ESOP 2015. Lecture Notes in Computer Science(), vol 9032. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-662-46669-8_9

https://link.springer.com/content/pdf/10.1007/978-3-662-46669-8_9.pdf

2. Hendrik van Antwerpen, Casper Bach Poulsen, Arjen Rouvoet, and Eelco Visser. 2018. Scopes as types. Proc. ACM Program. Lang. 2, OOPSLA, Article 114 (November 2018), 30 pages. https://doi.org/10.1145/3276484

"""
from scope_graph import ScopeGraph 
