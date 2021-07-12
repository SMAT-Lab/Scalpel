""" 
In this module, the single static assignment forms are  implemented to allow
futher anaysis. The module contain a single class named SSA.
"""
import ast
from ..core.vars_visitor import get_vars
from ..cfg.builder import CFGBuilder
from ..cfg.builder import Block
from ..core.mnode import MNode

BUILT_IN_FUNCTIONS = set([ "abs","delattr",
        "hash","memoryview","set","all","dict","help","min","setattr","any","dir","=hex","next","slice",
        "ascii","divmod","enumerate","id","object","sorted","bin","enumerate","input",
        "staticmethod","bool", "eval" "int" "open" "str" "breakpoint" "exec" "isinstance" "ord",
        "sum", "bytearray", "filter", "issubclass", "pow", "super", "bytes", "float", "iter", "print"
        "tuple", "callable", "format", "len", "property", "type", "chr","frozenset", "list", "range", "vars", 
        "classmethod", "getattr", "locals", "repr", "repr", "zip", "compile", "globals", "map", "reversed",  "__import__", "complex", "hasattr", "max", "round"]
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
        self.error_paths = []

    def get_global_live_vars(self):
        import_dict = self.m_node.parse_import_stmts()
        def_records = self.m_node.parse_func_defs()
        def_idents = [r['name'] for r in def_records if r['scope'] == 'mod']
        self.global_live_idents = def_idents + list(import_dict.keys())

    def get_assign_raw(self, stmts):
        """
        Retrieve the assignment statements 
        Args:
            stmts: A list of statements from the block node in the CFG.
        """
        assign_stmts = []
        for stmt in stmts:
            if isinstance(stmt,ast.Assign):
                for target in stmt.targets:
                    if hasattr(target, "id"):
                        assign_stmts.append((target, stmt.value))
            elif isinstance(stmt,ast.AnnAssign):
                if hasattr(stmt.target, "id"):
                    assign_stmts.append((stmt.target, stmt.value))
            elif isinstance(stmt, ast.AugAssign):
                if hasattr(stmt.target, "id"):
                    assign_stmts.append((stmt.target, stmt.value))
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if isinstance(stmt.value.func, ast.Attribute):
                    assign_stmts.append((None, stmt.value.func  ))
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value,
                    ast.Attribute):
                assign_stmts.append((None,  stmt))
            elif isinstance(stmt, ast.For):
                if isinstance(stmt.target, ast.Name):
                    assign_stmts.append((stmt.target,  stmt.iter))
                elif isinstance(stmt.target, ast.Tuple):
                    for item in stmt.target.elts:
                        assign_stmts.append((item,  stmt.iter))
            elif isinstance(stmt, ast.Import):
                for name in stmt.names:
                    if name.asname is not None:
                        assign_stmts.append((ast.Name(name.asname, ast.Store()),  None))
                    else:
                        assign_stmts.append((ast.Name(name.name, ast.Store()),  None))
                pass
            elif isinstance(stmt, ast.ImportFrom):
                for name in stmt.names:
                    if name.asname is not None:
                        assign_stmts.append((ast.Name(name.asname, ast.Store()),  None))
                    else:
                        assign_stmts.append((ast.Name(name.name, ast.Store()),  None))
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
        idents = []
        if ast_node is None:
            return idents
        if isinstance(ast_node, (ast.ListComp, ast.SetComp)):
            ast_node = ast_node.generators[0].iter
        for tmp_node in ast.walk(ast_node):
            if isinstance(tmp_node, ast.Name):
                idents.append(tmp_node.id)
        return idents

    def backward_query(self, block, ident_name, visited, path = []):
        phi_fun = []
        visited.add(block.id)
        path.append(block.id)
        # all the incoming path
        for suc_link in block.predecessors:
            is_this_path_done = False
            parent_block = suc_link.source
            # this is a back edge, discard it 
            #if parent_block.id > block.id:
            #    continue
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
                self.error_paths.append(path.copy())
            else:
                phi_fun += block_phi_fun
        path.pop()
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
        for block in all_blocks:
            #parse_vars from the right
            # single line function to be added 
            assign_records = self.get_assign_raw(block.statements)
            #call_stmts = self.get_attribute_stmts(block.statements)
            for ar in assign_records:
                left, right = ar
                if left == None:
                    continue
                actual_value = parse_val(right)
                if isinstance(left, ast.Tuple):
                    continue
                if left.id in self.numbering:
                    var_no = self.numbering[left.id]+1
                    self.numbering[left.id] = var_no
                    self.var_values[(left.id,var_no)] = actual_value
                else:
                    var_no = 1
                    self.numbering[left.id] = var_no
                    self.var_values[(left.id,var_no)] = actual_value
                phi_fun = []
                right_vars = self.get_identifiers(right)
                for var_name in right_vars:
                   # last assignment occur in the same block
                    for tmp_var_no in reversed(list(block.ssa_form.keys())):
                        if var_name == tmp_var_no[0]:
                            phi_fun.append(tmp_var_no)
                            break

                local_block_vars = [tmp[0] for tmp in phi_fun]
                remaining_vars = [tmp for tmp in right_vars if tmp not in local_block_vars]
                #  to look for the variable last assignment from incoming blocks
                phi_fun = []
                for var_name in remaining_vars:
                    visited = set()
                    phi_fun_incoming = self.backward_query(block, var_name, visited)
                    phi_fun += phi_fun_incoming
                block.ssa_form[(left.id, var_no)] = phi_fun
        self.ssa_blocks = all_blocks
        #for fun_name, fun_cfg in cfg.class_cfgs.items():
        #    print('----------', fun_name, '-------------')
        #    self.compute_SSA(fun_cfg)
        #for fun_name, fun_cfg in cfg.functioncfgs.items():
        #    print('----------', fun_name, '-------------')
        #    self.compute_SSA(fun_cfg)
        # to fix identifiers in the last block!!!!! such as ___author___
        #for ident_name, numbers in self.numbering.items():
        #    print(ident_name, numbers)

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

    def test(self, live_ident_table=[]):
        n_scopes = len(live_ident_table)
        for block in self.ssa_blocks:
            ident_phi_fun = {}
        
            for k, v in block.ssa_form.items():
                for item in v:
                    if item[0] not in ident_phi_fun:
                        ident_phi_fun[item[0]] = [item[1]]
                    else:
                        ident_phi_fun[item[0]] += [item[1]]
            for ident_name, numbers in ident_phi_fun.items():
                #print(ident_name)
                for i in range(n_scopes):
                    if ident_name in live_ident_table[-i] and -1 in live_ident_table[-i][ident_name]:
                        #print(ident_name, numbers)
                        return False
                    elif -1 in numbers and ident_name not in self.global_live_idents and ident_name not in BUILT_IN_FUNCTIONS:
                        return False
        #print(self.error_paths)
        return True
