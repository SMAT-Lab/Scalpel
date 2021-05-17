# this is the implementation of static single assignment
import ast
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
        # visit all blocks in bfs order 
        #cfg = CFGBuilder(self.module_ast)
        all_blocks = cfg.bfs()
        for block in all_blocks: 
            #parse_vars from the right
            assign_records = self.get_assign_raw(block.statements)
            for ar in assign_records:
                left, right = ar
                pass
                #print(ar)
        # visit each blocks of this 
        # numbering variables 
        # the final results of IR should be basic blocks

    def to_json(self):
        pass

