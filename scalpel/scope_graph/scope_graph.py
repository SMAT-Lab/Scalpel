import networkx as nx
import ast 
import queue

class ScopeGraph(ast.NodeVisitor):
    def __init__(self) -> None:
        """
        The central concepts in the framework are declarations, references, and scopes
        """
        self.sg = nx.DiGraph()  # scope graph
        self.ig = nx.DiGraph()  # inheritance graph
        self.imports = {}  # save information about imported names and scopes 
        self.MRO_graph = {}  # method resolution order
        self.parent_relations = {} # parent relations among scopes
        self.references = {}   # dictionary for refereced names 
        self.declarations = {} # dictionary for declared names 
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
        # let's ignore basename is in the form of X.B.C which is annolying 
        for bc in node.bases:
            if hasattr(bc, "id"):
                self.ig.add_edge(node.name, bc.id)
                if node.name in self.MRO_graph:
                    self.MRO_graph[node.name].append(bc.id)
                else:
                    self.MRO_graph[node.name] = [bc.id]


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

    def visit_Global(self, node):
        pass
    def visit_Nonlocal(self, node):
        pass 

    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname is not None:
                name = alias.asname
            else:
                name = alias.name
            self.imports[current_scope_name].append(alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.asname is not None:
                name = alias.asname
            else:
                name = alias.name
            self.imports[current_scope_name].append(alias.name)
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

    def print_out(self):

        print(self.MRO_graph)

        #for k, v in self.references.items():
        #    print(k, v )
        #for k, v in self.declarations.items():
        #    print(k, v )


    def MRO_resolve(self, start_name):
        if start_name not in self.MRO_graph:
            raise "Cannot locate the given name"

        init_names = self.MRO_graph[start_name] 
        
        cls_name_order = []
        is_visited = set() 
        dfs_queue = queue.Queue()

        for name in init_names:
            dfs_queue.put(name)
      
        while not dfs_queue.empty():
            cur_name = dfs_queue.get()
            if cur_name not in is_visited:
                is_visited.add(cur_name)
            else:
                continue 
            cls_name_order.append(cur_name)
            if cur_name in self.MRO_graph:
                tmp_names = self.MRO_graph[cur_name]
                for name in tmp_names:
                    dfs_queue.put(name) 
                
        #print(cls_name_order)
         
    
    def MRO_resolve_method(self, cls_name, method_name):
        """
        given current class name and method name;
        using method resolution order to locate which class the method name is defined 
        """
        if cls_name not in self.MRO_graph: 
            #raise Exception("Cannot locate the given name", cls_name)
            return None

        init_names = self.MRO_graph[cls_name]
        
        cls_name_order = []
        is_visited = set() 
        dfs_queue = queue.Queue()
        
        target_cls_name = None 

        for name in init_names:
            dfs_queue.put(name)

        while not dfs_queue.empty():
            cur_name = dfs_queue.get() 
            if cur_name not in is_visited:
                is_visited.add(cur_name)
            else:
                continue 
            cls_name_order.append(cur_name)
            if cur_name not in self.declarations:
                continue 
            if method_name in self.declarations[cur_name]:
                target_cls_name = cur_name
                break 

            if cur_name in self.MRO_graph:
                tmp_names = self.MRO_graph[cur_name]
                for name in tmp_names:
                    dfs_queue.put(name) 
        return target_cls_name

    def test(self):
        #print(self.MRO_garph 
        pass 

    def test_MRO_resolve(self, start_name):
        #self.MRO_resolve(start_name)
        target_cls_name = self.MRO_resolve_method("D", "rk")
        
        print(target_cls_name)
        pass 


# need to write resolve a method name 

def create_MRO():
    pass 

