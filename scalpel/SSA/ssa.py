""" 
In this module, the single static assignment forms are  implemented to allow
futher anaysis. The module contain a single class named SSA.
"""
import ast
from functools import reduce
from collections import OrderedDict
from ..core.vars_visitor import get_vars
from ..cfg.builder import CFGBuilder
from ..cfg.builder import Block
from ..core.mnode import MNode
from ..core.vars_visitor  import get_vars

BUILT_IN_FUNCTIONS = set([ "abs","delattr", "print", "str", "bin", "int",
        "float", "open",
        "hash","memoryview","set", "range", "self" "all","dict","help","min","setattr","any","dir","hex","next","slice", "self",
        "ascii","divmod","enumerate","id","object","sorted","bin","enumerate","input",
        "staticmethod","bool", "eval" "int", "len", "self", "open" "str" "breakpoint" "exec" "isinstance" "ord",
        "sum", "bytearray", "filter", "issubclass", "pow", "super", "bytes", "float", "iter", "print"
        "tuple", "callable", "format", "len", "property", "type", "chr","frozenset", "list", "range", "vars", 
        "classmethod", "getattr", "locals", "repr", "repr", "zip", "compile", "globals", "map", "reversed",  "__import__", "complex", "hasattr", "max", "round", "get_ipython"]
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

    def is_loop_header(block): 
        pass
    def compute_dominator():
        dominators = {}
        for block in self.ssa_blocks:
            dominaotrs[block.id] = [block.id]

        for block in self.ssa_blocks:
            dominaotrs[block.id] = [block.id]
            if len(block.predecessors)>=2:
                for p_link in block.predecessors:
                    p_block = p_link.source
                    #runner = p_block
    def is_dominator(self, b1, b2):
        # if b1 idom b2, all path has to go to b1 before accessing b2
        # then the in-degree of b2 must be one  and there exists an edge between b1-b2
        pass

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
        #if ident_name == 'wakeup_time':
        #    print('----------------1>')
        #    print(phi_fun)
        #    self.print_block(block)
        #    print('<----------------2')
        return phi_fun

    def compute_SSA(self, cfg, live_ident_table={}, is_final=False):
        """
        generate an SSA graph.
        """
        # to consider single line function call / single line attributes/
        # return statements
        self.get_global_live_vars()
        #self.numbering = {}
        # visit all blocks in bfs order 
        #cfg = CFGBuilder(self.module_ast)
        all_blocks = cfg.bfs()
        #print(len(all_blocks))
        self.compute_dom(all_blocks)
        for block in all_blocks:
            #parse_vars from the right
            # single line function to be added 
            assign_records = self.get_assign_raw(block.statements)
            #call_stmts = self.get_attribute_stmts(block.statements)
            for ar in assign_records:
                left, right = ar 
                actual_value = parse_val(right)
#                if isinstance(left, ast.Tuple):
#                    continue
                left_name = "<holder>"
                if left is not None:
                    left_name = left.id

                if left_name in self.numbering:
                    var_no = self.numbering[left_name]+1
                    self.numbering[left_name] = var_no
                    self.var_values[(left_name,var_no)] = actual_value
                else:
                    var_no = 1
                    self.numbering[left_name] = var_no
                    self.var_values[(left_name,var_no)] = actual_value
                phi_fun = []
                right_vars = self.get_identifiers(right)
                for var_name in right_vars:
                   # last assignment occur in the same block
                    #print(block.ssa_form.keys())
                    for tmp_var_no in reversed(list(block.ssa_form.keys())):
                        if var_name == tmp_var_no[0]:
                            phi_fun.append(tmp_var_no)
                            break
                local_block_vars = [tmp[0] for tmp in phi_fun]
                remaining_vars = [tmp for tmp in right_vars if tmp not in local_block_vars]
                # to look for the variable last assignment from incoming blocks
                phi_fun = []
                for var_name in remaining_vars:
                    visited = set()
                    phi_fun_incoming = self.backward_query(block, var_name, visited)
                    if len(phi_fun_incoming) == 0:
                        phi_fun += [(var_name, -1)]
                    else:
                        phi_fun += phi_fun_incoming

                block.ssa_form[(left_name, var_no)] = phi_fun


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
        self.dom = dom
        return dom
        # compute idom: immediately dominator
        idom = {}
        for block in ssa_blocks:
            idom[b.id] = set()
            pred_links = block.predecessors
            pred_nodes =  [pl.source for pl in pred_links]
            if len(pred_nodes)!=1:
                continue
            #if dom 
        # then compute the dominace frontiers
        dominance_frontier = {b.id:set() for b in ssa_blocks}
        for block in ssa_blocks:
            pred_links = block.predecessors
            pred_nodes =  [pl.source for pl in pred_links]
            if len(pred_nodes)<2:
                continue
            for pn in pred_nodes:
                runner = pn.id
                while runner != idom[b.id]:
                    dominance_frontier[runner].add(b.id)
                    runner = idom[runner]

        return dom

    def test(self, live_ident_table=[], def_names = []):
        n_scopes = len(live_ident_table)
        undefined_idents = []
        self.compute_dom(self.ssa_blocks)
        for block in self.ssa_blocks:
            ident_phi_fun = {} 
            for k, v in block.ssa_form.items():
                for item in v:
                    if item[0] not in ident_phi_fun:
                        ident_phi_fun[item[0]] = [item[1]]
                    else:
                        ident_phi_fun[item[0]] += [item[1]] 

            for ident_name, numbers in ident_phi_fun.items():
                if -1 not in numbers:
                    continue
                is_found = self.find_this_ident_name(ident_name, live_ident_table, def_names)
                if not is_found:
                    undefined_idents.append(ident_name) 
                    #self.print_block(block)
                    #print(ident_name, numbers)

        return undefined_idents
