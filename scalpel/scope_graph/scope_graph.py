import networkx as nx

"""
there are two types of edges between any two scopes : visiable and reachable 
"""

class ScopeGraph:
    def __init__(self) -> None:
        """
        The central concepts in the framework are declarations, references, and scopes
        """
        self.sg = nx.DiGraph()
        self.parent_relations = {} 
        self.references = {}   
        self.declarations = {}
        pass

    def resolve(name, working_scope):
        """
        Find the name in given working scope
        That is, a path with fewer parent transitions is more specific than a path with
        more parent transitions. 
        """
        pass 
    def add_scope(self, scope_name, parent_name):
        self._add_scope_name(scope_name, parent_name)
        
    def add_reference(self, scope_name, name, ctx):
        if ctx == "load":
            self.references[scope_name] = name 

        elif ctx == "del":
            # deletion operation is deemed as using the reference
            self.references[scope_name] = name 
 
        elif ctx == "store":
            self._add_declared()
            self.declarations[scope_name] = name 

        else:
            raise "Unknown context for given name reference"

    def _add_contained(self):
        pass 

    def _add_declared(self):
        pass

    def get_parent(self, scope_name):
        #map scope to its parent scope 
        if scope_name in self.parent_relations:
            return self.parent_relations[scope_name]
        raise "Failed to locate parent scope!"



