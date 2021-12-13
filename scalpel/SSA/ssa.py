""" 
In this module, the single static assignment forms are  implemented to allow
futher anaysis. The module contain a single class named SSA.
"""
import ast
import astor
from functools import reduce
from collections import OrderedDict
import networkx as nx
from ..core.vars_visitor import get_vars
from ..cfg.builder import CFGBuilder, Block, invert
from ..core.mnode import MNode
from ..core.vars_visitor  import get_vars

BUILT_IN_FUNCTIONS = { 
         ### built-in functions
         "iteritems",
        "abs","delattr", "print", "str", "bin", "int", "xrange", "eval", "all", "exit", "basestring"
        "float", "open", "unicode", "exec", "breakpoint", "cmp",
        "hash","memoryview","set", "tuple", "range", "self" "all","dict","help","min","setattr","any","dir","hex","next","slice", "self",
        "ascii","divmod","enumerate","id", "isinstance", "object","sorted","bin","enumerate","input",
        "staticmethod","bool", "eval" "int", "len", "self", "open" "str" "breakpoint" "exec" "isinstance" "ord",
        "sum", "bytearray", "filter", "issubclass", "pow", "super", "bytes", "float", "iter", "print"
        "tuple", "callable", "format", "len", "property", "type", "chr","frozenset", "list", "range", "vars", 
        "classmethod", "getattr", "locals", "repr", "repr", "zip", "compile", "globals", "map", "reversed",  "__import__", "complex", "hasattr", "max", "round", "get_ipython",
        "ord",
        ###  built-in exceptions
        "BaseException", "SystemExit", "KeyboardInterrupt", "GeneratorExit", "Exception",
        "StopIteration", "StopAsyncIteration","ArithmeticError", "FloatingPointError", "OverflowError",
        "ZeroDivisionError","AssertionError", "AttributeError", "BufferError", "EOFError",
        "ImportError", "ModuleNotFoundError", "LookupError", "IndexError" , "KeyError", "MemoryError", "NameError",
        "UnboundLocalError", "OSError", "IOError", "BlockingIOError", "ChildProcessError", "ConnectionError",
        "BrokenPipeError", "ConnectionAbortedError", "ConnectionRefusedError","ConnectionResetError",
        "FileExistsError", "FileNotFoundError", "InterruptedError","IsADirectoryError", "NotADirectoryError",
        "PermissionError","ProcessLookupError", "TimeoutError", "ReferenceError", "RuntimeError",
        "NotImplementedError","RecursionError", "SyntaxError", "IndentationError", "TabError", "EnvironmentError",
        "SystemError", "TypeError", "ValueError","UnicodeError","UnicodeDecodeError","UnicodeEncodeError","UnicodeTranslateError",
        # built-in warnings
        "Warning","DeprecationWarning","PendingDeprecationWarning","RuntimeWarning","SyntaxWarning",
        "UserWarning", "FutureWarning","ImportWarning","UnicodeWarning","BytesWarning","ResourceWarning",
        # Others
        "NotImplemented", "__main__", "__doc__", "__file__", "__name__", "__debug__", "__class__", "__name__"
        "__version__", "__all__",  "__docformat__", "__package__"
        }


def parse_val(node):
    # does not return anything
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Str):
        if hasattr(node, "value"):
            return node.value
        else:
            return node.s
    return "other"


class SSA:
    """
    Build SSA graph from a given AST node based on the CFG.
    """
    def __init__ (self, src):
        """
        Args:
            src: the source code as input.
        """
        # the class SSA takes a module as the input 
        self.src = src   # source code
        self.module_ast = ast.parse(src)
        self.numbering = {}  # numbering variables
        self.var_values = {}  # numbering variables
        self.m_node = MNode("tmp")
        self.m_node.source = self.src
        self.m_node.gen_ast() 
        self.global_live_idents = []
        self.ssa_blocks = []
        self.error_paths = {}
        self.dom = {}

        self.block_ident_gen = {}
        self.block_ident_use = {}
        self.reachable_table = {}
        id2block = {}
        self.unreachable_names = {}
        self.undefined_names_from = {}
        self.global_names = []

    def get_global_live_vars(self):
        #import_dict = self.m_node.parse_import_stmts()
        #def_records = self.m_node.parse_func_defs()
        #def_idents = [r['name'] for r in def_records if r['scope'] == 'mod']
        #self.global_live_idents = def_idents + list(import_dict.keys())
        self.global_live_idents = []

    def flatten_tuple(ast_tuple):
        """
        input: ast tuple object
        return a list of elements in the given tuple
        """
        output =[]
        first = ast_tuple[0]
        second = ast_tuple[1]

    def get_attribute_stmts(self, stmts):
        call_stmts = []
        for stmt in stmts:
            if isinstance(stmt,ast.Call) and isinstance(stmt.func, ast.Attribute):
                call_stmts += [stmt]

    def get_identifiers(self, ast_node):
        """
        Extract all identifiers from the given AST node.
        Args:
            ast_node: AST node.
        """
        if ast_node is None:
            return []
        res = get_vars(ast_node)
        idents = [r['name'] for r in res if  r['name'] is not None and "." not in r['name']]
        return idents

    def get_stmt_idents_ctx(self, stmt, del_set=[]):
        # if this is a definition of class/function, ignore
        stored_idents = []
        loaded_idents = []
        func_names = []
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            stored_idents.append(stmt.name)
            func_names.append(stmt.name)
            #for arg in stmt.args.args: 
            #    if isinstance(arg.annotation, ast.Name):
            #        loaded_idents.append(arg.annotation.id)
            #    if isinstance(arg.annotation, ast.Attribute):
            #        if isinstance(arg.annotation.value, ast.Name):
            #            loaded_idents.append(arg.annotation.value.id)
            new_stmt = stmt
            new_stmt.body = []
            ident_info = get_vars(new_stmt)
            for r in ident_info:
                if r['name'] is None or "." in r['name'] or "_hidden_" in r['name']:
                    continue
                if r['usage'] == "load":
                    loaded_idents.append(r['name']) 
            return stored_idents, loaded_idents, func_names
        
        if isinstance(stmt, ast.ClassDef):
            stored_idents.append(stmt.name)
            func_names.append(stmt.name)
            return stored_idents, loaded_idents, func_names


        # if this is control flow statements, we should not visit its body to avoid duplicates
        # as they are already in the next blocks

        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            for alias in stmt.names:
                if alias.asname is None:
                    stored_idents += [alias.name.split('.')[0]]
                else:
                    stored_idents += [alias.asname.split('.')[0]]
            return stored_idents, loaded_idents, []

        if isinstance(stmt, (ast.Try)):
            for handler in stmt.handlers:
                if handler.name is not None:
                    stored_idents.append(handler.name)
                    #print(ast.dump())
                if isinstance( handler.type, ast.Name):
                    loaded_idents.append(handler.type.id)
                elif isinstance( handler.type, ast.Attribute) and isinstance(handler.type.value, ast.Name):
                    loaded_idents.append(handler.type.value.id)
            return stored_idents, loaded_idents, []
        if isinstance(stmt, ast.Global):
            for name in stmt.names:
                self.global_names.append(name)
            return stored_idents, loaded_idents, []

        visit_node = stmt
        if isinstance(visit_node,(ast.If, ast.IfExp)):
            #visit_node.body = []
            #visit_node.orlse=[]
            visit_node = stmt.test

        if isinstance(visit_node,(ast.With)):
            visit_node.body = []
            visit_node.orlse=[]

        if isinstance(visit_node,(ast.While)):
            visit_node.body = []
        if isinstance(visit_node,(ast.For)):
            visit_node.body = []

        ident_info = get_vars(visit_node)
        for r in ident_info:
            if r['name'] is None or "." in r['name'] or "_hidden_" in r['name']:
                continue
            if r['usage'] == 'store':
                stored_idents.append(r['name'])
            else:
                loaded_idents.append(r['name'])
            if r['usage'] == 'del':
                del_set.append(r['name'])
        return stored_idents, loaded_idents, []

    def compute_undefined_names(self, cfg, scope=["mod"]):
        """
        generate undefined names from given cfg
        """ 
        all_blocks = cfg.get_all_blocks()
        reachable_table = {}
        id2block = {}
        block_ident_gen = {}
        block_ident_use = {}
        block_ident_unorder = {}
        block_ident_del = {}

        subscope_undefined_names = []
        undefined_names_table = [] 
        undefined_names = []
        scope_str  = ".".join(scope)

        dom = self.compute_dom_old(all_blocks) 
        #idom = self.compute_idom(all_blocks) 
        for block in all_blocks:
            #assign_records = self.get_assign_raw(block.statements)
            id2block[block.id] = block
            block_ident_gen[block.id] = []
            block_ident_use[block.id] = []
            block_ident_unorder[block.id] = []
            block_ident_del[block.id] = []
            ident_to_be_traced = []
            del_set = []
            for stmt in block.statements:
                stored_idents, loaded_idents, scope_func_names = self.get_stmt_idents_ctx(stmt, del_set=del_set) 
                for ident in loaded_idents:
                    if ident[0:8] == "_hidden_":
                        # this is noise
                        continue
                    if ident not in block_ident_gen[block.id] and ident not in stored_idents:
                        ident_to_be_traced.append({
                                        "name":ident, 
                                        "scope": scope_str, 
                                        "type":"unresolved",
                                        "path_id": [], 
                                        "path_src": []
                                    }
                                )
                block_ident_gen[block.id] += stored_idents
                block_ident_unorder[block.id]  += scope_func_names
            block_ident_use[block.id]  = ident_to_be_traced 
            block_ident_del[block.id]  = del_set
        for block in all_blocks:
            # number of stmts parsed
            for stmt in block.statements:
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    fun_undefined_names = self.compute_undefined_names(cfg.functioncfgs[(block.id, stmt.name)], scope = scope+[stmt.name])  
                    fun_args = cfg.function_args[(block.id, stmt.name)]
                    # exclude arguments 
                    #fun_undefined_names = [name for name in fun_undefined_names if name not in tmp_avail_names] 
                    fun_idx = block_ident_gen[block.id].index(stmt.name)
                    part_ident_gen = block_ident_gen[block.id][0:fun_idx]
                    # arguments its own name + part of gen set and unorder func/class/def names
                    tmp_avail_names = fun_args + [stmt.name] + block_ident_unorder[block.id] +part_ident_gen
                    fun_undefined_names = [name for name in fun_undefined_names if name["name"] not in tmp_avail_names]
                    subscope_undefined_names += fun_undefined_names

                elif isinstance(stmt, ast.ClassDef):
                    class_cfg = cfg.class_cfgs[stmt.name]
                    cls_body_undefined_names = self.compute_undefined_names(class_cfg, scope = scope+[stmt.name])
                    cls_idx = block_ident_gen[block.id].index(stmt.name)
                    part_ident_gen = block_ident_gen[block.id][0:cls_idx] 

                    tmp_avail_names = part_ident_gen + [stmt.name] + block_ident_unorder[block.id]
                    cls_body_undefined_names = [name for name in cls_body_undefined_names if name["name"] not in tmp_avail_names]
                    subscope_undefined_names += cls_body_undefined_names
            # process this block
            block_id = block.id
            all_used_idents = block_ident_use[block_id]+subscope_undefined_names
            #all_used_idents = []
            idents_non_local = [ident for ident in all_used_idents if ident["name"] not in BUILT_IN_FUNCTIONS and ident["name"] not in self.global_names and ident["type"] == "unresolved"]
            idents_non_local = idents_non_local
            idents_left = []
            dominators = dom[block_id]

            for ident in idents_non_local:
                ident_name = ident["name"]
                is_found = False
                # look for this var in it dominatores
                for d_b_id in dominators:
                    if d_b_id == block_id:
                        continue
                    if ident_name in block_ident_gen[d_b_id] and ident_name not in block_ident_del[d_b_id]:
                        is_found = True
                        break
                if is_found == False:
                    idents_left.append(ident)
                # for those vars that cannot be found in its domiators, backtrace to 
                # test if there is a path along wich the var is not defined. 
            path_constraint = None
            if len(block.predecessors) ==1:
                path_constraint = block.predecessors[0].exitcase
            for ident in idents_left:
                visited = set()
                exec_path = []
                is_not_found = self.backward_query_new(block, ident["name"], visited, dom=dom, path=exec_path, block_ident_gen=block_ident_gen, condition_cons=path_constraint,
                        entry_id=cfg.entryblock.id, block_ident_del=block_ident_del)
                if is_not_found:
                    #ident["path_id"].append(exec_path)
                    #ident["path_src"].append([self.print_block(id2block[e_id]) for e_id in exec_path])
                    is_found_here = self.hit_scope(ident['name'], block_ident_gen, block_ident_unorder)
                    if is_found_here:
                        if scope_str == ident["scope"]:
                            ident["type"] = "local"
                        else:
                            ident["type"] = "foreign"
                    undefined_names += [ident]
                    #if  ident[0] == "cell_data":
                    #    print(self.print_block(block))
        return undefined_names

    # if there exists one path that ident_name is not reachable 
    # when the entered block is the entry block, it means the variable has not been found in this path. 
    #Otherwise, the algorithm terminates at a previous block.
    def backward_query_new(self, block, ident_name, visited, path = [], dom={},idom = {}, dom_stmt_res = [],  block_ident_gen={},  block_ident_del= {}, condition_cons=None, entry_id=1):
        # condition constraints:
        visited.add(block.id)
        path += [block.id]
        # all the incoming path
        # if this is the entry block and ident not in the gen set then return True
        if block.id == entry_id:
            return True

        for suc_link in block.predecessors:
            if condition_cons is not None and suc_link.exitcase is not None: 
                this_condition = invert(condition_cons) 
                this_txt = astor.to_source(this_condition) 
                this_edge_txt = astor.to_source(suc_link.exitcase)
                # this path contracdict the constraints
                if this_txt.strip()==this_edge_txt.strip():
                    continue
            parent_block = suc_link.source
            target_block = suc_link.target
            # deal with cycles, this is back edge
            if parent_block is None:
                continue
            if parent_block.id in visited or parent_block.id == block.id:
                continue
            # if the block dominates the parent block, then give it up
            if parent_block.id in dom and  block.id in dom[parent_block.id]:
                continue
            ##############
            if parent_block.id not in block_ident_gen:
                continue
            # if the name id found in this gen set. then stop visiting this path
            if ident_name in block_ident_gen[parent_block.id]:
                continue
            if parent_block.id in block_ident_del and ident_name in block_ident_del[parent_block.id]:
                path.append(entry_id)
                return True
            # if the name id is not found in the parent block and the parent is entry  return True
            if parent_block.id == entry_id:
                path.append(entry_id)
                return True
            # if continue to search
            # not in its parent gen set  then search from this path
            return self.backward_query_new(parent_block, ident_name, visited, dom=dom, block_ident_gen=block_ident_gen, condition_cons=condition_cons, entry_id=entry_id, path = path) 
        return False

    def hit_scope(self, ident_name, block_ident_gen, block_ident_unorder):
        gen_sets = list(block_ident_gen.values()) + list(block_ident_unorder.values())
        return any(ident_name in g_s for g_s in gen_sets)

    def is_undefined(self, load_idents):
        ident_phi_fun = {}
        for item in load_idents:
            if item[0] in ident_phi_fun:
                pass

    def to_json(self):
        pass

    def print_block(self, block):
        #for stmt in block.statements:
        #print(block.get_source())
        return block.get_source()

    # compute the dominators 
    def compute_idom(self, ssa_blocks):
        # construct the Graph
        entry_block = ssa_blocks[0]
        G = nx.DiGraph()
        for block in ssa_blocks: 
            G.add_node(block.id)
            exits = block.exits
            preds =  block.predecessors
            for link in preds+exits:
                G.add_edge(link.source.id, link.target.id)
        #DF = nx.dominance_frontiers(G, entry_block.id)
        idom = nx.immediate_dominators(G, entry_block.id)
        return idom

    def RD(self, cfg_blocks):
        # worklist 
        # this is to express the conventional RD anaysis
        # By using Out and Kill set to compute the latest assignment to a variable  
        entry_block = cfg_blocks[0]
        Out[entry_block.id]  = set()
        # init the iterative algorithm
        for block in cfg_blocks:
            if block.id != entry_block.id:
                out[block.id] = set()
        changed = True
        while changed:
            for block in cfg_blocks:
                # 
                pre_links = block.predecessors
                pre_blocks = [pl.source for pl in pre_links]
                pre_outs = [out[pb.id] for pb in pre_blocks]
                In[block.id] =  reduce(set.intersection, pre_outs) 
                Out[block.id] = gen(B) (In[block.id]-kill[block.id])
        # boundry
        return 0

    def compute_dom_old(self, ssa_blocks):
        entry_block = ssa_blocks[0]
        id2blocks = {b.id:b for b in ssa_blocks}
        block_ids = list(id2blocks.keys())
        entry_id = entry_block.id
        N_blocks = len(ssa_blocks)
        dom = {}
        # for all other nodes, set all nodes as the dominators
        for b_id in block_ids:
            if b_id == entry_id:
                dom[b_id] = set([entry_id])
            else:
                dom[b_id] = set(block_ids)
        # Iteratively eliminate nodes that are not dominators
        #Dom(n) = {n} union with intersection over Dom(p) for all p in pred(n)
        changed = True
        counter = 0
        while changed:
            changed = False
            for b_id in block_ids:
                if b_id == entry_id:
                    continue
                pre_block_ids = [pre_link.source.id for pre_link in id2blocks[b_id].predecessors ]
                pre_dom_set = [dom[pre_b_id] for pre_b_id in pre_block_ids if pre_b_id in dom]
                new_dom_set = set([b_id])

                if len(pre_dom_set) != 0:
                    new_dom_tmp = reduce(set.intersection, pre_dom_set) 
                    new_dom_set = new_dom_set.union(new_dom_tmp)
                old_dom_set = dom[b_id]

                if new_dom_set != old_dom_set:
                    changed = True
                    dom[b_id] = new_dom_set
        return dom

