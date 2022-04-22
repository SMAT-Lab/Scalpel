"""
Neron, P., Tolmach, A., Visser, E., Wachsmuth, G. (2015). A Theory of Name Resolution. In: Vitek, J. (eds) Programming Languages and Systems. 
ESOP 2015. Lecture Notes in Computer Science(), vol 9032. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-662-46669-8_9

https://link.springer.com/content/pdf/10.1007/978-3-662-46669-8_9.pdf

"It can be illuminating to depict a scope graph graphically. In a scope graph diagram, a scope is depicted as a circle, a reference as a
box with an arrow pointing into the scope that contains it, and a declaration as"

"""
import networkx as nx

"""
there are two types of edges between any two scopes : visiable and reachable 
"""

class ScopeGraph:
    def __init__(self) -> None:
        self.sg = nx.DiGraph()
        pass

    def resolve(name, working_scope):
        """
        Find the name in given working scope
        """
        pass 
    def add_scope(self, scope_name, parent_name):
        self._add_scope_name(scope_name, parent_name)
        
    def add_reference(self, scope, name, ctx):
        if ctx == "load":
            self._add_contained()
            pass
        elif ctx == "del":
            # deletion operation is deemed as using the reference
            self._add_declared()
            pass 
        elif ctx == "store":
            self._add_declared()
            pass
        else:
            raise "Unknown context for given name reference"

    def _add_contained(self):
        pass 

    def _add_declared(self):
        pass

    def get_parent(self):
        #map scope to its parent scope 
        pass 
