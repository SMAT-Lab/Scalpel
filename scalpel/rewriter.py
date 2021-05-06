import os
import sys
import ast

# In python there are in total 23 statements to be considered 
# the user must specify the match pattern as well as insert pattern
# for instance.
# it can be  Call - >  another_callname for instance
# the given new stmt must be clearly linked to the original stmt if it needs
# such information
# for example, if the we have an assignment named a = 10 
# then we need to consturct an output stmt as print(a)
# then the new pattern for the output should be Callstmt:args = [stmt.left[0]]
# now the first step is to insert an stmt
# the second step is to think about how to write template rules
# make it easy, format string! such as the new stmt =
# "print("","").format(stmt.targets[0])

class Rewriter(ast.NodeVisitor):
    def __init__(self,src, pattern, new_stmt):
        # pattern
        self.pattern = pattern
        self.new_stmt = new_stmt
        self.src = src
        self.ast = None
        self.ast = ast.parse(self.src, mode='exec')
    def search_for_pos(self, stmt_lst, pattern): 
        for i, stmt in enumerate(stmt_lst):
            if pattern(stmt):
                return i
        return -1

    # once or all 
    def insert(self):
        assert self.ast is not None
        assert isinstance(self.ast, ast.Module)
        self.insert_after()
    # once or all

    def insert_before(self, loc=""):
        assert self.ast is not None
        assert isinstance(self.ast, ast.Module)
        pos = self.search_for_pos(self.ast.body, self.pattern)
        if pos<0:
            return self.ast

        call_node = ast.Call(ast.Name(id='print',ctx=ast.Load()),
                [ast.Constant("testing", None)], [])
        new_stmt = ast.Expr(call_node)

        self.ast.body.insert(pos, new_stmt)
        self.ast = ast.fix_missing_locations(self.ast)
        return self.ast

    def insert_after(self):
        assert self.ast is not None
        assert isinstance(self.ast, ast.Module)
        pos = self.search_for_pos(self.ast.body, self.pattern)
        new_stmt = ast.Call(ast.Name(id='print',ctx=ast.Load()),
                [ast.Name(id="testing", ctx=ast.Load())], [])
        self.ast.body.insert(pos+1, new_stmt)
        self.ast =  ast.fix_missing_locations(self.ast)

    def remove(self):
        assert self.ast is not None
        assert isinstance(self.ast, ast.Module)
        pos = self.search_for_pos(self.ast.body, self.pattern)
        if pos<0:
            return self.ast
        del self.ast.body[pos] 
        self.ast =  ast.fix_missing_locations(self.ast)
        return self.ast

    def replace(self):
        assert self.ast is not None
        assert isinstance(self.ast, ast.Module)
        pos = self.search_for_pos(self.ast.body, self.pattern)
        if pos<0:
            return self.ast
        call_node = ast.Call(ast.Name(id='print',ctx=ast.Load()),
                [ast.Constant("testing1", None)], [])
        new_stmt = ast.Expr(call_node)
        self.ast.body[pos] = new_stmt
        return ast.fix_missing_locations(self.ast)

    def visit_FunctionDef(self, node):
        pass
    def visit_AsyncFunctionDef(self, node):
        pass
    def visit_ClassDef(self, node):
        pass
    def visit_Return(self, node):
        pass
    def visit_Delete(self, node):
        pass
    def visit_Assign(self, node):
        pass
    def visit_AugAssign(self, node):
        pass
    def visit_AnnAssign(self, node):
        pass
    def visit_For(self, node):
        pass
    def visit_AsyncFor(self, node):
        pass
    def visit_While(self, node):
        pass
    def visit_If(self, node):
        pass
    def visit_With(self, node):
        pass
    def visit_AsyncWith(self, node):
        pass
    def visit_Raise(self, node):
        pass
    def visit_Try(self, node):
        pass
    def visit_Assert(self, node):
        pass
    def visit_Import(self, node):
        pass
    def visit_ImportFrom(self, node):
        pass
    def visit_Global(self, node):
        pass
    def visit_Nonlocal(self, node):
        pass
    def visit_Expr(self, node):
        pass
    def visit_Pass(self, node):
        pass
    def visit_Break(self, node):
        pass
    def visit_Continue(self, node):
        pass

