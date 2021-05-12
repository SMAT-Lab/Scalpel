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

    def rewrite(self):
        self.generic_visit(self.ast)
        return ast.fix_missing_locations(self.ast)

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

    def visit_Name(self, node):
        if node.id in self.pattern['Name']:
            new_name = self.pattern['Name'][node.id]
            node.id = new_name
    def visit_Attribute(self, node):
        self.generic_visit(node)
        return node
    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        return node

    def get_func_name(self, node):
        if hasattr(node, "id"):
            return node.id
        elif hasattr(node,"attr"):
            return self.get_func_name(node.value)+"."+node.attr
        else:
            pass

    def visit_Call(self, node):
        func_name = self.get_func_name(node.func)
        if func_name in self.pattern["Call"]:
            new_func_name = self.pattern["Call"][func_name]
            if new_func_name is None:
                return None
            node.func.id = new_func_name


        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        return node

    def visit_Return(self, node):
        self.generic_visit(node)
        return node

    def visit_Delete(self, node):
        self.generic_visit(node)
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        return node

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        self.generic_visit(node)
        return node

    def visit_For(self, node):
        self.generic_visit(node)
        return node

    def visit_AsyncFor(self, node):
        self.generic_visit(node)
        return node

    def visit_While(self, node):
        self.generic_visit(node)
        return node

    def visit_If(self, node): 
        if "if" in self.pattern["Stmt"]:
            alt_stmt = self.pattern["Stmt"]["if"]
            if alt_stmt is None:
                return None

        self.generic_visit(node)

        return node
    def visit_IfExp(self, node): 
        if "if" in self.pattern["Stmt"]:
            alt_stmt = self.pattern["Stmt"]["if"]
            if alt_stmt is None:
                return None
        self.generic_visit(node)
        return node
    def visit_With(self, node):
        self.generic_visit(node)
        return node

    def visit_AsyncWith(self, node):
        self.generic_visit(node)
        return node

    def visit_Raise(self, node):
        self.generic_visit(node)
        return node

    def visit_Try(self, node):
        self.generic_visit(node)
        return node
    def visit_Assert(self, node):
        self.generic_visit(node)
        return node
    def visit_Import(self, node):
        self.generic_visit(node)
        return node
    def visit_ImportFrom(self, node):
        self.generic_visit(node)
        return node
    def visit_Global(self, node):
        self.generic_visit(node)
        return node
    def visit_Nonlocal(self, node):
        self.generic_visit(node)
        return node
    def visit_Expr(self, node):
        self.generic_visit(node)
        return node
    def visit_Pass(self, node):
        self.generic_visit(node)
        return node
    def visit_Break(self, node):
        self.generic_visit(node)
        return node
    def visit_Continue(self, node):
        self.generic_visit(node)
        return node

