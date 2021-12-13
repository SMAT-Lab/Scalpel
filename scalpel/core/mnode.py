"""
In this module, Scalplel provides the interface to users. Each of Python source
files are fed into this module to generate an frontend object for both parsing
and code instrumentation. In addition, scope information can also be given for
fine-grained operations. 
"""
import ast
from ..core.vars_visitor import get_vars
from ..core.func_call_visitor import get_func_calls
from scalpel.core.util import UnitWalker
from ..cfg.builder import CFGBuilder


def get_attr_name (node):
    if isinstance(node, ast.Call):
        # to be test
        return get_attr_name(node.func)
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return get_attr_name(node.value)+"."+node.attr
    elif isinstance(node, ast.Subscript):
        return get_attr_name(node.value)


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
        Returns a list of variable records ranking by their line numbers
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
        Returns a list of function calls ranking by their line numbers
        Args:
            scope: a dotted string to provide name space. For instance, A.fun
            means to retreive the function named fun in the class A
        """
        wanted_ast = self._retrieve_by_scope(self.ast, scope)
        results =  get_func_calls(wanted_ast)
        return results

    def gen_ast(self):
        """
        Build AST tree for th source 
        """
        try:
            self.ast = ast.parse(self.source)
        except Exception as e:
            self.ast = None

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
                def_info = {"scope":scope, "name": node.name, "arg": [], "kws": [],
                        "lineno":node.lineno, "col_offset":node.col_offset}
                def_records.append(def_info)
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
        if scope == "":
            return target_search_node
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
        #cfg = CFGBuilder().build("toy", self.module_ast)
        #cfg.build_visual('cfg', 'pdf')
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

    def parse_import_stmts(self):
        """
        Return a dictionary data structure to map the imported name, from which
        module and its aliases.
        """
        import_stmts = []
        for stmt in self.ast.body:
            if isinstance(stmt, (ast.ImportFrom, ast.Import)):
                import_stmts += [stmt]

        import_dict = {}
        for stmt in import_stmts:
            if isinstance(stmt, ast.Import):
                items = [nn.__dict__ for nn in stmt.names]
                for d in items:
                    if d['asname'] is None:  # alias name not found, use its imported name
                        import_dict[d['name']] = d['name']
                    else:
                        import_dict[d['asname']] = d['name'] # otherwise , use alias name
            if isinstance(stmt, ast.ImportFrom):
                m_name = stmt.module
                if m_name is None and stmt.level== 1:
                    m_name = '.'
                if m_name is None and stmt.level== 2:
                    m_name = '..' 
                items = [nn.__dict__ for nn in stmt.names]
                for d in items:
                    if d['asname'] is None: # alias name not found
                        import_dict[d['name']] = m_name +'.'+d['name']
                    else:
                        import_dict[d['asname']] = m_name +'.'+d['name']
        return import_dict

    def retrieve_meta(self, node):
        results = {"assign_pairs":[], "other_calls":[]}
        assign_pairs = []
        other_calls  = []
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
            else:
                call_lst = get_func_calls(node)
                if call_lst not in other_calls:
                    other_calls.append(call_lst)

        results["assign_pairs"]  = assign_pairs
        results["other_calls"]  = other_calls
        return results 

    def _process_base_names(self, bases):
        base_names = []
        for b_node in bases:
            if isinstance(b_node, ast.Name):
                base_names.append(b_node.id)
            elif isinstance(b_node, ast.Attribute):
                base_names.append(get_attr_name(b_node))
        return base_names

    #def parse_function_body(self):
    #    """
    #    Prase all function/class definitions
    #    """
    #    func_records = {}
    #    base_records = {}
    #    for stmt in self.ast.body:
    #        if isinstance(stmt, ast.FunctionDef):
    #            func_records[stmt.name] = self.retrieve_meta(stmt)
    #        if isinstance(stmt, ast.ClassDef):
    #            base_records[stmt.name] = self._process_base_names(stmt.bases)
    #            for c_stmt in stmt.body:
    #                if isinstance(c_stmt, ast.FunctionDef):
    #                    func_records[stmt.name+'.' + c_stmt.name] = self.retrieve_meta(c_stmt)
    #    return func_records, base_records

    def gen_cfg(self):
        cfg = CFGBuilder().build("", self.ast)
        return cfg

    def make_unit_walker(self):
        """
        Returns a generator of units at statement level
        """
        return UnitWalker(self.ast)
