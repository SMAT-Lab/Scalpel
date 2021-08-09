""" 
In this module, the single static assignment forms are  implemented to allow
futher anaysis. The module contain a single class named SSA.
"""
import ast
from functools import reduce
from collections import OrderedDict
import networkx as nx
from ..core.vars_visitor import get_vars
from ..cfg.builder import CFGBuilder, Block
from ..core.mnode import MNode
from ..core.vars_visitor  import get_vars

BUILT_IN_FUNCTIONS = set([ "abs","delattr", "print", "str", "bin", "int", "xrange", "eval", "all", "__name__",
        "float", "open",
        "hash","memoryview","set", "tuple", "range", "self" "all","dict","help","min","setattr","any","dir","hex","next","slice", "self",
        "ascii","divmod","enumerate","id", "isinstance", "object","sorted","bin","enumerate","input",
        "staticmethod","bool", "eval" "int", "len", "self", "open" "str" "breakpoint" "exec" "isinstance" "ord",
        "sum", "bytearray", "filter", "issubclass", "pow", "super", "bytes", "float", "iter", "print"
        "tuple", "callable", "format", "len", "property", "type", "chr","frozenset", "list", "range", "vars", 
        "classmethod", "getattr", "locals", "repr", "repr", "zip", "compile", "globals", "map", "reversed",  "__import__", "complex", "hasattr", "max", "round", "get_ipython",
        
        "ImportError", "KeyError", "ModuleNotFoundError", "TypeError",
        "ValueError",
        "Exception", "DeprecationWarning",
        "display" # notebook functions 
        ]
        )

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


    def get_assign_raw(self, stmts):
        """
        Retrieve the assignment statements 
        Args:
            stmts: A list of statements from the block node in the CFG.
        """
        assign_stmts = []
        for stmt in stmts:
            if isinstance(stmt,ast.Assign):
                if isinstance(stmt.targets, list):
                    for target in stmt.targets:
                        if hasattr(target, "id"):
                            assign_stmts.append((target, stmt.value))
                        elif isinstance(target, ast.Tuple):
                            for elt in target.elts:
                                if hasattr(elt, "id"):
                                    assign_stmts.append((elt, stmt.value))

            elif isinstance(stmt,ast.AnnAssign):
                if hasattr(stmt.target, "id"):
                    assign_stmts.append((stmt.target, stmt.value))
            elif isinstance(stmt, ast.AugAssign):
                if hasattr(stmt.target, "id"):
                    assign_stmts.append((stmt.target, stmt.value))
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if isinstance(stmt.value.func, ast.Attribute):
                    assign_stmts.append((None, stmt.value  ))
                else:
                    assign_stmts.append((None, stmt.value  ))
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value,
                    ast.Attribute):
                assign_stmts.append((None,  stmt))
            elif isinstance(stmt, ast.For):
                if isinstance(stmt.target, ast.Name):
                    assign_stmts.append((stmt.target,  stmt.iter))
                elif isinstance(stmt.target, ast.Tuple):
                    for item in stmt.target.elts:
                        if isinstance(item, ast.Tuple):
                            for elt in item.elts:
                                assign_stmts.append((elt,  stmt.iter))
                        else:
                            assign_stmts.append((item,  stmt.iter))
            elif isinstance(stmt, ast.Import):
                for name in stmt.names:
                    if name.asname is not None:
                        assign_stmts.append((ast.Name(name.asname, ast.Store()),  None))
                    else:
                        assign_stmts.append((ast.Name(name.name, ast.Store()),  None))
            elif isinstance(stmt, ast.ImportFrom):
                print(ast.dump(stmt))
                for name in stmt.names:

                    if name.asname is not None:
                        assign_stmts.append((ast.Name(name.asname, ast.Store()),  None))
                    else:
                        assign_stmts.append((ast.Name(name.name, ast.Store()),  None))
            elif isinstance(stmt, ast.Return):
                    assign_stmts.append((None,  stmt.value))
            elif isinstance(stmt, ast.FunctionDef):
                    assign_stmts.append((ast.Name(stmt.name, ast.Store()),  None))
            elif isinstance(stmt, ast.ClassDef):
                    assign_stmts.append((ast.Name(stmt.name, ast.Store()),  None))
            elif isinstance(stmt, ast.With):
                    for item in stmt.items:
                        # left: optional_vars  right: context_expr
                        assign_stmts.append((item.optional_vars, item.context_expr))

        return assign_stmts

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


    def backward_query(self, block, ident_name, visited, path = []):
        phi_fun = []
        visited.add(block.id)
        path.append(block.id)
        # all the incoming path
        for suc_link in block.predecessors: 
            is_this_path_done = False 
            parent_block = suc_link.source
            target_block = suc_link.target
            # deal with cycles, this is back edge
            if parent_block is None:
                continue
            if parent_block.id in visited or parent_block.id == block.id:
                continue

            # if the block dominates the parent block, then give it up
            if parent_block.id in self.dom and  block.id in self.dom[parent_block.id]:
                continue

            #grand_parent_blocks = [link.source for link in parent_block.predecessors]
            #grand_parent_block_ids = [b.id for b in grand_parent_blocks]
            #if block.id in grand_parent_block_ids:
            #    continue
            #if ident_name == 'condition':
                #print('testing')
                #self.print_block(parent_block)
            target_ssa_left = reversed(list(parent_block.ssa_form.keys())) 
            block_phi_fun = []
            for tmp_var_no in target_ssa_left:
                if tmp_var_no[0] == ident_name:
                    block_phi_fun.append(tmp_var_no) 
                    is_this_path_done = True
                    break
            # this is one block 
            #phi_fun += block_phi_fun
            if is_this_path_done:
                phi_fun += block_phi_fun
                continue
            if len(block_phi_fun) == 0:
                # not found in this parent_block
                if len(parent_block.predecessors)!=0 and parent_block.id not in visited:
                    block_phi_fun = self.backward_query(parent_block,
                            ident_name, visited, path = path)
                    #phi_fun += block_phi_fun
            #else:
            #    phi_fun += block_phi_fun
            if len(block_phi_fun) == 0:
                phi_fun += [(ident_name, -1)]
                if ident_name in self.error_paths:
                    self.error_paths[ident_name].append(path.copy())
                else:
                    self.error_paths[ident_name] = [path.copy()]
            else:
                phi_fun += block_phi_fun
        path.pop()
        return phi_fun

    def get_stmt_idents_ctx(self, stmt):
        # if this is a definition of class/function, ignore
        stored_idents = []
        loaded_idents = []
        if isinstance(stmt, (ast.FunctionDef, ast.ClassDef)):
            # todo, values to named params
            stored_idents.append(stmt.name)
            return stored_idents, loaded_idents

        # if this is control flow statements, we should not visit its body to avoid duplicates
        # as they are already in the next blocks

        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            for alias in stmt.names:
                if alias.asname is None:
                    stored_idents += [alias.name.split('.')[0]]
                else:
                    stored_idents += [alias.asname.split('.')[0]]
            return stored_idents, loaded_idents

        if isinstance(stmt, (ast.Try)):
            for handler in stmt.handlers:
                if handler.name is not None:
                    stored_idents.append(handler.name)
            return stored_idents, loaded_idents

        visit_node = stmt
        if isinstance(visit_node,(ast.If, ast.IfExp)):
            visit_node.body = []
            visit_node.orlse=[]
        if isinstance(visit_node,(ast.With)):
            visit_node.body = []
            visit_node.orlse=[]

        if isinstance(visit_node,(ast.While)):
            visit_node.body = []

        ident_info = get_vars(visit_node)
        for r in ident_info:
            if r['name'] is None or "." in r['name']:
                continue
            if r['usage'] == 'store':
                stored_idents.append(r['name'])
            else:
                loaded_idents.append(r['name'])
        return stored_idents, loaded_idents

    def compute_undefined_names(self, cfg, scope="mod"):
        """
        generate undefined names from given cfg
        """
        all_blocks = cfg.get_all_blocks()
        reachable_table = {}
        id2block = {}

        block_ident_gen = {}
        block_ident_use = {}

        dom = self.compute_dom_old(all_blocks) 
        for block in all_blocks:
            #assign_records = self.get_assign_raw(block.statements)
            id2block[block.id] = block
            block_ident_gen[block.id] = []
            block_ident_use[block.id] = []
            ident_to_be_traced = []
            for stmt in block.statements:
                stored_idents, loaded_idents = self.get_stmt_idents_ctx(stmt) 
                for ident in loaded_idents:
                    # cannot find in previous statements or current statements
                    if ident not in stored_idents and ident not in block_ident_gen[block.id]:
                        ident_to_be_traced.append(ident)
                block_ident_gen[block.id] += stored_idents
            block_ident_use[block.id]  = ident_to_be_traced

        subscope_undefined_names = []
        undefined_names = [] 
        for block in all_blocks:
            # number of stmts parsed
            for stmt in block.statements:
                if isinstance(stmt, ast.FunctionDef):
                    fun_undefined_names = self.compute_undefined_names(cfg.functioncfgs[stmt.name])  
                    fun_args = cfg.function_args[stmt.name]
                    # exclude arguments 
                    fun_undefined_names = [name for name in fun_undefined_names if name not in fun_args]
                    subscope_undefined_names += fun_undefined_names
                if isinstance(stmt, ast.ClassDef):
                    class_cfg = cfg.class_cfgs[stmt.name]
                    for inside_fun_name, inside_fun_cfg in class_cfg.functioncfgs.items():
                        fun_args = class_cfg.function_args[inside_fun_name]
                        fun_undefined_names = self.compute_undefined_names(inside_fun_cfg) 
                        fun_undefined_names = [name for name in fun_undefined_names if name not in fun_args]
                        subscope_undefined_names += fun_undefined_names
            subscope_undefined_names = [name for name in subscope_undefined_names if name not in block_ident_gen[block.id]]
            # process this block
            block_id = block.id 
            all_used_idents = block_ident_use[block_id]+ list(set(subscope_undefined_names))
            idents_non_local = [ident for ident in all_used_idents if ident not in BUILT_IN_FUNCTIONS]
            idents_non_local = list(set(idents_non_local))

            idents_left = []

            dominators = dom[block_id]

            for ident in idents_non_local:
                is_found = False
                # look for this var in it dominatores
                for d_b_id in dominators:
                    if d_b_id == block_id:
                        continue
                    if ident in block_ident_gen[d_b_id]:
                        is_found = True
                        break
                if is_found == False:
                    idents_left.append(ident)
                # for those vars that cannot be found in its domiators, backtrace to 
                # test if there is a path along wich the var is not defined. 
            for ident in idents_left:
                visited = set()
                is_found = self.backward_query_new(block, ident, visited, dom={}, block_ident_gen=block_ident_gen) 
                if not is_found:
                    undefined_names += [ident]
        return list(set(undefined_names))


    def backward_query_new(self, block, ident_name, visited, path = [], dom={}, block_ident_gen={}):
        phi_fun = []
        visited.add(block.id)
        path.append(block.id)
        # all the incoming path
        for suc_link in block.predecessors: 
            is_this_path_done = False 
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
            if ident_name in block_ident_gen[parent_block.id]:
                return True
            return self.backward_query_new(parent_block, ident_name, visited, dom=dom, block_ident_gen=block_ident_gen)

        return False

    def compute_SSA(self, cfg, live_ident_table={}, is_final=False):
        """
        generate an SSA graph.
        """
        # to consider single line function call / single line attributes/
        # return statements
        self.get_global_live_vars()
        #self.numbering = {}
        # visit all blocks in bfs order 
        all_blocks = cfg.get_all_blocks()
        self.compute_dom(all_blocks)
        for block in all_blocks:
            #assign_records = self.get_assign_raw(block.statements)
            ident_records = self.get_stmt_idents_ctx(block.statements)
            for stored_idents, loaded_idents in ident_records:
                phi_fun = []
                for var_name in loaded_idents:
                   # last assignment occur in the same block
                    for tmp_var_no in reversed(list(block.ssa_form.keys())):
                        if var_name == tmp_var_no[0]:
                            phi_fun.append(tmp_var_no)
                            break
                local_block_vars = [tmp[0] for tmp in phi_fun]
                remaining_vars = [tmp for tmp in loaded_idents if tmp not in local_block_vars and (tmp not in stored_idents)]
                phi_fun = []
                for var_name in remaining_vars:
                    visited = set()
                    phi_fun_incoming = self.backward_query(block, var_name, visited)
                    if len(phi_fun_incoming) == 0:
                        phi_fun += [(var_name, -1)]
                    else:
                        phi_fun += phi_fun_incoming
                if len(stored_idents) == 0:
                    stored_idents += ["<holder>"]
                    #block.ssa_form[("<holder>", 1)] = phi_fun
                    #continue

                for ident_name in stored_idents:
                    if ident_name in self.numbering:
                        var_no = self.numbering[ident_name]+1
                        self.numbering[ident_name] = var_no
                    #    self.var_values[(left_name,var_no)] = actual_value
                        block.ssa_form[(ident_name, var_no)] = phi_fun
                    else:
                        var_no = 1
                        self.numbering[ident_name] = var_no
                        block.ssa_form[(ident_name, var_no)] = phi_fun
                        #    self.var_values[(left_name,var_no)] = actual_value

            #call_stmts = self.get_attribute_stmts(block.statements)
            #for ar in assign_records:
            #    left, right = ar 
            #    actual_value = parse_val(right)
#                if isinstance(left, ast.Tuple):
#                    continue
            #    left_name = "<holder>"
            #    if left is not None:
            #        left_name = left.id
            #
            #    if left_name in self.numbering:
            #        var_no = self.numbering[left_name]+1
            #        self.numbering[left_name] = var_no
            #        self.var_values[(left_name,var_no)] = actual_value
            #    else:
            #        var_no = 1
            #        self.numbering[left_name] = var_no
            #        self.var_values[(left_name,var_no)] = actual_value
            #    phi_fun = []
            #    right_vars = self.get_identifiers(right)
            #    for var_name in right_vars:
            #       # last assignment occur in the same block
            #        #print(block.ssa_form.keys())
            #        for tmp_var_no in reversed(list(block.ssa_form.keys())):
            #            if var_name == tmp_var_no[0]:
            #                phi_fun.append(tmp_var_no)
            #                break
            #    local_block_vars = [tmp[0] for tmp in phi_fun]
            #    remaining_vars = [tmp for tmp in right_vars if tmp not in local_block_vars]
            #    # to look for the variable last assignment from incoming blocks
            #    phi_fun = []
            #    for var_name in remaining_vars:
            #        visited = set()
            #        phi_fun_incoming = self.backward_query(block, var_name, visited)
            #        if len(phi_fun_incoming) == 0:
            #            phi_fun += [(var_name, -1)]
            #        else:
            #            phi_fun += phi_fun_incoming

            #    block.ssa_form[(left_name, var_no)] = phi_fun
        self.ssa_blocks = all_blocks

    def is_undefined(self, load_idents):
        ident_phi_fun = {}
        for item in load_idents:
            if item[0] in ident_phi_fun:
                pass

    def to_json(self):
        pass

    def build_viz(self):
        pass

    def compute_final_idents(self):
        # when there is only one exit block, compute SSA for all the vars in
        # numbering make a if statement here to see if this is a module
        final_phi_fun = {}
        def_reach = {}
        for block in self.ssa_blocks:
            if len(block.exits) == 0:
                #for ident_name, phi_rec in block.ssa_form.items():
                #    print(ident_name, phi_rec)
                for ident_name, number in self.numbering.items():
                    visited = set()
                    phi_fun_incoming = self.backward_query(block, ident_name, visited)
                    if ident_name not in def_reach:
                        def_reach[ident_name] = set([tmp[1] for tmp in phi_fun_incoming])
                #for ident_name, nums in def_reach.items():
                #    print(ident_name, set(nums))
        return def_reach

    def find_this_ident_name(self, ident_name, live_ident_table, def_names):
        n_scopes = len(live_ident_table)
        for i in range(n_scopes):
            if ident_name in live_ident_table[-i]:
                if (-1 in live_ident_table[-i][ident_name]):
                    return False
                else:
                    return True
        if ident_name in BUILT_IN_FUNCTIONS:
            return True
        if ident_name not in def_names:
            return False
        return True

    def retrieve_key_stmts(self, block_id_lst):
        import astor
        id2blocks = {b.id:b for b in self.ssa_blocks}
        for b_id in block_id_lst:
            tmp_block = id2blocks[b_id]
            key_stmt = tmp_block.statements[-1]
            #print(astor.to_source(key_stmt))

    def print_block(self, block):
        #for stmt in block.statements:
        print(block.get_source())

    # compute the dominators 
    def compute_dom(self, ssa_blocks):
        # construct the Graph
        #
        entry_block = ssa_blocks[0]
        G = nx.DiGraph()
        for block in ssa_blocks: 
            G.add_node(block.id)
            exits = block.exits
            preds =  block.predecessors
            for link in preds+exits:
                G.add_edge(link.source.id, link.target.id)
        DF = nx.dominance_frontiers(G, entry_block.id)
        return DF 

    def RD(self, cfg_blocks):
        # worklist 
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

    #def test(self, live_ident_table=[], def_names = []):
    #    n_scopes = len(live_ident_table)
    #    undefined_idents = []
    #    def_use = {}
    #    for block in self.ssa_blocks:
    #        ident_phi_fun = {}
    #        for k, v in block.ssa_form.items():
    #            for item in v:
    #                if item[0] not in ident_phi_fun:
    #                    ident_phi_fun[item[0]] = [item[1]]
    #                else:
    #                    ident_phi_fun[item[0]] += [item[1]] 
    #        for ident_name, numbers in ident_phi_fun.items():
    #            if -1 not in numbers:
    #                continue
    #            is_found = self.find_this_ident_name(ident_name, live_ident_table, def_names)
    #            if not is_found:
    #                undefined_idents.append(ident_name) 
    #            else: 
    #                pass
                   #
                   # if ident_name == 'np':
                   #     print(live_ident_table)
                   #     self.print_block(block)
    #    return undefined_idents
