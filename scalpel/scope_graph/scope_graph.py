import networkx as nx
import ast 
"""
there are two types of edges between any two scopes : visiable and reachable 
"""

# set an current scope for scope information records,

# when entering the scope, parent scope relationship is formed.
# now for each of names 


class ScopeGraph(ast.NodeVisitor):
    def __init__(self) -> None:
        """
        The central concepts in the framework are declarations, references, and scopes
        """
        self.sg = nx.DiGraph()
        self.parent_relations = {} 
        self.references = {}   
        self.declarations = {}
        self.current_scope_name = None
        pass

    def build(self, ast_tree):
        self.visit(ast_tree)
        pass 

    def visit_FunctionDef(self, node):
        self.declarations[self.current_scope_name].append(node.name)
        
        save_scope_name = self.current_scope_name
        self.current_scope_name = node.name

        if self.current_scope_name not in self.references:
            self.references[self.current_scope_name] = []

        if self.current_scope_name not in self.declarations:
            self.declarations[self.current_scope_name] = []

        self.generic_visit(node)
        self.current_scope_name = save_scope_name
        return node 

    def visit_ClassDef(self, node):
        self.declarations[self.current_scope_name].append(node.name)
        
        save_scope_name = self.current_scope_name
        self.current_scope_name = node.name

        if self.current_scope_name not in self.references:
            self.references[self.current_scope_name] = []

        if self.current_scope_name not in self.declarations:
            self.declarations[self.current_scope_name] = []

        self.generic_visit(node)
        self.current_scope_name = save_scope_name
        return node

    def visit_Module(self, node):
        save_scope_name = self.current_scope_name
        self.current_scope_name = "Mod"

        if self.current_scope_name not in self.references:
            self.references[self.current_scope_name] = []

        if self.current_scope_name not in self.declarations:
            self.declarations[self.current_scope_name] = []

        self.generic_visit(node)
        self.current_scope_name = save_scope_name
        return node
    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Load, ast.Del)):
            # this is 
            self.references[self.current_scope_name].append(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.declarations[self.current_scope_name].append(node.id)

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

    def print_out(self):
        for k, v in self.references.items():
            print(k, v )
        for k, v in self.declarations.items():
            print(k, v )


