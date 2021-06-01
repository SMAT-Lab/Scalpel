"""
In this module, Scalplel provides the interface to users. Each of Python soure
files are fed into this module to generate an front end object for both parsing
and code instrumentation. In addition, scope information can also be given for
fine-grained operations. 
"""
import ast
import os
import re
import sys
import json
from queue import Queue
from copy import deepcopy
from ..core.vars_visitor import get_vars
from ..core.func_call_visitor import get_func_calls
from scalpel.core.util import UnitWalker

class ImportRelation:

    def __init__(self):
        self.path = []
        self.src : MNode
        self.dest:MNode
        self.payload = [] 
        self.stmts = []

class MNode:
    """
    Build a Module node  of the given input source file with publicaly APIs to
    manipulate for parsing and  code instrumentation
    file.

    """

    def __init__(self, name):
        """
        Args:
            name: The filename of the input source file.
        """
        self.name = name
        self.full_name = ""
        self.children = []
        self.parent = None
        self.source = ''
        self.ast = None
        self.class_pair = None
        self.node_type_dict = None
        self.node_type_gt = None
        self.call_links = None 

    def __str__(self):
        """
        returns an string representation of the object
        """
        return str(self.name)

    def rewrite(self, scope = "mod"):
        """
        rewrite code
        """
        pass

    def _read_scope(self, scope):
        pass

    def parse_vars(self, scope = ""):
        """
        Return a list of variable records ranking by their line numbers
        Args:
            scope: a dotted string to provide name space. For instance, A.fun
            means to retreive the function named fun in the class A
        """

        if scope == "":
            results = get_vars(self.ast)
            return results
        wanted_ast = self._retrieve_by_scope(self.ast, scope)
        results = get_vars(wanted_ast)
        return results
    def gen_import_relations():
        pass

    def parse_func_calls(self, scope = ""):

        """
        Return a list of function calls ranking by their line numbers
        Args:
            scope: a dotted string to provide name space. For instance, A.fun
            means to retreive the function named fun in the class A
        """
        if scope == "":
            results = get_vars(self.ast)
            return results
        wanted_ast = self._retrieve_by_scope(self.ast, scope)
        results =  get_func_calls(wanted_ast)
        return results

    def gen_ast(self):
        """
        Build AST tree for th source 
        """
        self.ast = ast.parse(self.source)

    def _parse_func_defs(self, ast_node_lst, def_records, scope = "mod"):
        """
        Parse the function and class definitions in this module
        Args:
            ast_node_lst: a list of statements to be visited.
            def_records: a list of dictionary, each of whose entry is a
            function/class definition.
            scope: the scope that is currently being visited. When it is "mod",
            it is visiting under the entire module.

        """

        for node in ast_node_lst:
            def_info = {}
            if isinstance(node, ast.FunctionDef):
                def_info = {"scope":scope, "name": node.name, "arg": [], "kws": [],
                        "lineno":node.lineno, "col_offset":node.col_offset}
                def_records.append(def_info)
                self._parse_func_defs(node.body, def_records, scope=node.name)

            elif isinstance(node, ast.ClassDef):
                #visit class body
                # to consider class records
                self._parse_func_defs(node.body, def_records, scope=node.name)
                pass
            # assignment statements are useful for assignment graph
            elif isinstance(node, ast.Assign):
                pass
            elif isinstance(node, ast.AugAssign):
                pass
            elif isinstance(node, ast.AnnAssign):
                pass

    def _retrieve_by_scope(self, target_search_node, scope):
        """
        retrieve an AST node by the scope directive. 
        Args:
            target_search_node: the AST node to be examined for entries in the
            given scope.
            function/class definition.
            scope: a dotted string to provide name space. For instance, A.fun
            means to retreive the function named fun in the class A

        """
        if hasattr(target_search_node, "name") and target_search_node.name == scope:
            return target_search_node
        for node in target_search_node.body:
            def_info = {}
            if isinstance(node, ast.FunctionDef):
                if node.name == scope:
                    return node
                if scope.split('.')[0] == node.name:
                    return self._retrieve_by_scope(node, scope.lstrip(node.name+'.')) 

            elif isinstance(node, ast.ClassDef):
                #visit class body
                # to consider class records
                if node.name == scope:
                    return node
                if scope.split('.')[0] == node.name:
                    return self._retrieve_by_scope(node, scope.lstrip(node.name+'.'))

            # assignment statements are useful for assignment graph
            elif isinstance(node, ast.Assign):
                pass
            elif isinstance(node, ast.AugAssign):
                pass
            elif isinstance(node, ast.AnnAssign):
                pass

    def parse_func_defs(self):
        """
        Return a list of dictionaries, each of its item is a dictionary of
        function/class definition information.
        """
        # mod : module 
        # func: function
        def_records = []
        self._parse_func_defs(self.ast.body, def_records, scope = "mod")
        return def_records

    def parse_import_stmt(self):
        """
        Return a dictionary data structure to map the imported name, from which
        module and its aliases.
        """
        import_stmts = []
        for stmt in self.ast.body:
            if isinstance(stmt, (ast.ImportFrom, ast.Import)):
                import_stmt += [stmt]

        import_dict = {}
        for stmt in import_stmts:
            if isinstance(node, ast.Import):
                items = [nn.__dict__ for nn in node.names]
                for d in items:
                    if d['asname'] is None:  # alias name not found, use its imported name
                        import_dict[d['name']] = d['name']
                    else:
                        import_dict[d['asname']] = d['name'] # otherwise , use alias name
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                # for import from statements
                # module names are the head of a API name
                items = [nn.__dict__ for nn in node.names]
                for d in items:
                    if d['asname'] is None: # alias name not found
                        import_dict[d['name']] = node.module+'.'+d['name']
                    else:
                        import_dict[d['asname']] = node.module+'.'+d['name']

    def parse_Assigns(node):
        assign_pairs = []
        for node in ast.walk(node):
            if isinstance(node, ast.Assign):
                call_lst = get_func_calls(node.value)
                for target in node.targets:
                    var_info = get_vars(target)[0]
                    assign_pairs += [{"var":var_info, "calls":call_lst}]

            elif isinstance(node, ast.AnnAssign):
                call_lst = get_func_calls(node.value)
                var_name = get_vars(node.target)[0]
                assign_pairs += [{"var":var_info, "calls":call_lst}]

            elif isinstance(node, ast.AugAssign):
                call_lst = get_func_calls(node.value)
                var_name = get_vars(node.target)[0]
                assign_pairs += [{"var":var_info, "calls":call_lst}]
        return assign_pairs
    

    def make_unit_walker(self):
        """
        Returns a generator of units at statement level
        """
        return UnitWalker(self.ast)
 

class ModuleGraph:
    # ep: entry point
    def __init__(self, ep, top_level_name):
        self.ep = ep
        self.top_level_name = top_level_name
        self.root_node = None
        self.mnodes = []

    def __len__():
        return len(self.mnodes)

    def build(self):
        cwd = os.getcwd() # save current working dir
        os.chdir(self.ep)
        os.chdir("..")
        self.root_node = MNode(self.top_level_name)
        self.build_dir_tree(self.root_node)

    def build_dir_tree(self, node):
        if os.path.isdir(node.name) is True:
            os.chdir(node.name)
            items  = os.listdir('.')
            for item in items:
                child_node = MNode(item)
                child_node.parent =  node
                self.build_dir_tree(child_node)
                node.children.append(child_node)
            os.chdir('..')
        else:
            # this is a file
            if node.name.endswith('.py'):
                source = open(node.name, 'rb').read()
                node.source = source.decode("utf-8", errors="ignore")

    def parse_import(self, tree):
        module_item_dict = {}
        try:
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module is None and node.level not in module_item_dict:
                        module_item_dict[node.level] = []
                    elif node.module not in module_item_dict:
                       module_item_dict[node.module] = []
                    items = [nn.__dict__ for nn in node.names] 
                    for d in items:
                        if node.module is None:
                            module_item_dict[node.level].append(d['name'])
                        else:
                            module_item_dict[node.module].append(d['name'])

            return module_item_dict
        except(AttributeError):
            return None 


    def leaf2root(self, node):
        tmp_node = node
        path_to_root = []
        # not init.py
        while tmp_node is not None:
            path_to_root.append(tmp_node.name)
            tmp_node = tmp_node.parent
        if node.name == '__init__.py':
            #path_to_root = path_to_root[1:]
            path_name = ".".join(reversed(path_to_root))
            return path_name
        else:
            path_name = ".".join(reversed(path_to_root[1:]))
            path_name = "{}.{}".format(path_name, node.name.split('.')[0])
            return path_name

    def find_child_by_name(self, node, name):
        for ch in node.children:
            if ch.name == name:
                return ch
        return None

    def find_node_by_name(self, nodes, name):
        for node in nodes:
            if node.name == name or node.name.rstrip('.py')== name:
                return node
        return None

    def go_to_that_node(self,  cur_node, visit_path):
        # current_node 
        # visit_path
        route_length = len(visit_path)
        tmp_node = None
        if route_length == 0:
            return self.root
            #return tmp_node

        # go to the siblings of the current node
        # this is the topmost node
        if cur_node.parent is None:
            return tmp_node

        tmp_node =  self.find_node_by_name(cur_node.parent.children, visit_path[0])
        if tmp_node is not None:
            for i in range(1,route_length):
                tmp_node =  self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
        # from the topmost, this rule for Pandas or django  
        # this is normally the case of absolute import
        elif visit_path[0] == self.root.name:
            tmp_node = self.root
            for i in range(1,route_length):
                tmp_node =  self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
            return tmp_node
        # from its parent 
        elif visit_path[0] == cur_node.parent.name:
            tmp_node = cur_node.parent
            for i in range(1,route_length):
                tmp_node =  self.find_node_by_name(tmp_node.children, visit_path[i])
                if tmp_node is None:
                    break
        # we are still in the directory
        if tmp_node is not None and tmp_node.name.endswith('.py') is not True:
           tmp_node =  self.find_node_by_name(tmp_node.children, '__init__.py')

        return tmp_node

    def tree_infer_levels(self, root_node):
        API_name_lst = []
        leaf_stack = []
        working_queue = []
        working_queue.append(root_node)
        all_nodes = []
        all_edges = []
        # bfs to search all I leafs

        while len(working_queue)>0:
            tmp_node = working_queue.pop(0)
            if tmp_node.name.endswith('.py') == True:
                leaf_stack.append(tmp_node)
            working_queue.extend(tmp_node.children)

        # visit all elements from the stack
        for node in leaf_stack:
            # private modules
            if node.name!='__init__.py' and node.name[0]=='_':
                continue
            module_item_dict = parse_import(node.ast)
            if module_item_dict is None:
                continue

            for k, v in module_item_dict.items():
                if k is None or isinstance(k, int):
                    continue
                dst_node = go_to_that_node(root_node, node, k)
                if dst_node  is not None:
                    # from to 
                    all_edges += [(dst_node.full_name, node.full_name)]
        #print(len(all_edges))
        all_edges = list(set(all_edges))

        for node in leaf_stack:
            if node.class_pair is not None:
                for ch_class,parent_class in node.class_pair.items():
                    if parent_class is None:
                        continue
                    if parent_class in node.cargo:
                        for k, v in node.cargo[parent_class].items():
                            if k not in node.cargo[ch_class]:  # child class
                                node.cargo[ch_class][k] = v
            API_prefix = leaf2root(node)

        return API_name_lst

def process_single_module(module_path):
    API_name_lst = []
    # process other modules !!!
    if os.path.isfile(module_path):
        pass
        #name_segments =  os.path.basename(module_path).rstrip('.py*') # .py and .pyx
        # process a single file module
        #res, tree = extract_class(module_path)
        #node_API_lst = make_API_full_name(res, name_segments)
        #API_name_lst.extend(node_API_lst)
    else:
        first_name = os.path.basename(module_path)
        working_dir = os.path.dirname(module_path)
        path = []
        cwd = os.getcwd() # save current working dir
        os.chdir(working_dir)
        root_node = Tree(first_name)
        build_dir_tree(root_node)
        API_name_lst = tree_infer_levels(root_node)
        os.chdir(cwd) # go back cwd

    return API_name_lst

#def process_lib_single():
#    l_name = sys.argv[1]
    #all_lib_dir = '/data/sdb/jiawei/lib_history'
#    API_data = {"module":[], "API":{}, "version":[]}
#    lib_dir = os.path.join(all_lib_dir, l_name)
#    versions = os.listdir(lib_dir)
#    versions.sort(key=lambda x:parse_version(x))
#    API_data['version'] = versions
    #for v in versions[-1:]:
#    for v in versions:
#        v_dir = os.path.join(lib_dir, v)
#        entry_points  = process_wheel(v_dir, l_name)
#        if entry_points is None:
#            continue
#        API_data['module'] = entry_points
#        for ep in entry_points:
#          API_name_lst = process_single_module(ep)  # finish one version 
#          if API_name_lst is None:
#              continue
#          for name in API_name_lst:
              # why it is None
#              # matplotlib
#              if name not in API_data['API']:
#                  API_data['API'][name] = [v]
#              else:
#                  API_data['API'][name] += [v]
    #print(len(API_data['API']))
#    # finish all versions for a single one
#    f = open("new_data/{}.json".format(l_name), 'w')
#    f.write(json.dumps(API_data))
#    f.close()


