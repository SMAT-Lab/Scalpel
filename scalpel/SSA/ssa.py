# this is the implementation of static single assignment
import ast
from ..core.vars_visitor import get_vars
from ..cfg.builder import CFGBuilder
from ..cfg.builder import Block


class SSA:

    def __init__ (self, src):
        # the class SSA takes a module as the input 
        self.src = src
        self.module_ast = ast.parse(src)
        self.numbering = {}

    def get_assign_raw(self, stmts):
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

        return assign_stmts

    def gen(self):
        cfg = CFGBuilder().build("toy", self.module_ast)
        #cfg.build_visual('cfg.pdf', 'pdf')
        # visit all blocks in bfs order 
        #cfg = CFGBuilder(self.module_ast)
        all_blocks = cfg.bfs()
        for block in all_blocks:
            #parse_vars from the right
            assign_records = self.get_assign_raw(block.statements)
            for ar in assign_records:
                left, right = ar
                if left.id in self.numbering:
                    var_no = self.numbering[left.id]+1
                    self.numbering[left.id] = var_no
                else:
                    var_no = 1
                    self.numbering[left.id] = var_no
                #self.rewrite_right(right)
                new_right = []
                right_vars = get_vars(right)
                for var_name in right_vars:
                    tmp_right = []
                    # last assignment occur in the same block
                    if var_name in block.ssa_form:
                        pass
                        continue

                    for suc_link in block.exits:
                        if var_name in suc_link.target.ssa_form:
                            tmp_right += [var_name, suc_link.target.ssa_form[var_name][0]]
                    if len(tmp_right) == 0:
                        pass
                    if len(tmp_right)==1:
                        right = []
                        # normal case
                    elif len(tmp_right)>1:
                        # phi function insertion
                        pass

                block.ssa_form[left.id] = (var_no, right) 

    def to_json(self):
        pass

