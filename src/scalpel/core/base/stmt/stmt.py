'''
This specification is from https://docs.python.org/3/library/ast.html
stmt = FunctionDef(identifier name, arguments args,
                    stmt* body, expr* decorator_list, expr? returns,
                    string? type_comment)
        | AsyncFunctionDef(identifier name, arguments args,
                            stmt* body, expr* decorator_list, expr? returns,
                            string? type_comment)

        | ClassDef(identifier name,
            expr* bases,
            keyword* keywords,
            stmt* body,
            expr* decorator_list)
        | Return(expr? value)

        | Delete(expr* targets)
        | Assign(expr* targets, expr value, string? type_comment)
        | AugAssign(expr target, operator op, expr value)
        -- 'simple' indicates that we annotate simple name without parens
        | AnnAssign(expr target, expr annotation, expr? value, int simple)

        -- use 'orelse' because else is a keyword in target languages
        | For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        | AsyncFor(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        | While(expr test, stmt* body, stmt* orelse)
        | If(expr test, stmt* body, stmt* orelse)
        | With(withitem* items, stmt* body, string? type_comment)
        | AsyncWith(withitem* items, stmt* body, string? type_comment)

        | Match(expr subject, match_case* cases)

        | Raise(expr? exc, expr? cause)
        | Try(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
        | TryStar(stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody)
        | Assert(expr test, expr? msg)

        | Import(alias* names)
        | ImportFrom(identifier? module, alias* names, int? level)

        | Global(identifier* names)
        | Nonlocal(identifier* names)
        | Expr(expr value)
        | Pass | Break | Continue
'''

from _ast import AST, Assign, SetComp
from enum import Enum
from abc import ABC, abstractmethod
import ast
from typing import Any 
import astor

class SStmt:
  
    def __init__(self, node):
        assert isinstance(node, ast.stmt)
        self.node = node
        self.src = astor.to_source(node)
        self.node_lineno =node.lineno
        self.node_col_offset = node.col_offset 
    
    def get_line_number(self):
        """
        return the location of this statement represented by lineno and column offset
        """
        return (self.node_lineno, self.node_col_offset)
    
    def get_src(self):
        return self.src 
    
    @abstractmethod
    def get_clauses():
        # return a dictionary:  name, clauses
        # for an assignment stmt can be: target: stmt.target, value: stmt.value 
        raise NotImplemented
    
class AssignStmt(SStmt):
 
    # overriding abstract method
    def get_clauses():
        raise NotImplemented
    
    def get_line_number(self):
        return super().get_line_number()

class AugAssignStmt(SStmt):
 
    # overriding abstract method
    def get_line_number(self):
        return super().get_line_number()
    
class AnnStmt(SStmt):
 
    # overriding abstract method   
    def get_line_number(self):
        return super().get_line_number()
    def get_clauses():
        raise NotImplemented
    
    
class IfStmt(SStmt):
 
    def get_line_number(self):
        return super().get_line_number()
    def get_clauses():
        raise NotImplemented
    
        
class ForStmt(SStmt):
 
    # overriding abstract method
    
    def get_line_number(self):
        return super().get_line_number()
    def get_clauses():
        raise NotImplemented
    
    
class WhileStmt(SStmt):
 
    # overriding abstract method
    def get_line_number(self):
        return super().get_line_number()
    
    def get_clauses():
        raise NotImplemented
    
class FunctionDedfStmt(SStmt):  # overriding abstract method
    def get_line_number(self):
        return super().get_line_number()
    
    def get_clauses():
        raise NotImplemented
      
class ClassDefStmt(SStmt):
    # overriding abstract method
    def get_line_number(self):
        return super().get_line_number()
    def get_clauses():
        raise NotImplemented
     
class MatchDefStmt(SStmt):
    # overriding abstract method    
    def get_line_number(self):
        return super().get_line_number()
    def get_clauses():
        raise NotImplemented

class TryStmt(SStmt):
    # overriding abstract method    
    def get_line_number(self):
        return super().get_line_number()
    def get_clauses():
        raise NotImplemented
    
class ReturnStmt(SStmt):
    # overriding abstract method   
    def get_line_number(self):
        return super().get_line_number()
    def get_clauses():
        raise NotImplemented

class StmtVisitor(ast.NodeVisitor):
    
    def visit(self, node: AST) -> Any:
        self.sstmt_lst = [] 
        return super().visit(node)
    
    def visit_FunctionDef(self, node):
        print(ast.dump(node))
        return node

    def visit_ClassDef(self, node):
        # let's ignore basename is in the form of X.B.C which is annolying
        print(ast.dump(node))
        return node

   
    def visit_Global(self, node):
        pass

    def visit_Nonlocal(self, node):
        pass

    def visit_Import(self, node):
        pass 

    def visit_ImportFrom(self, node):
        pass 
    def visit_Assign(self, node: Assign) -> Any:
        self.sstmt_lst.append(AssignStmt(node))
        return node 
    
    def visit_AnnAssign(self, node: Assign) -> Any:
        self.sstmt_lst.append(AnnStmt(node))
        
        return node
    def visit_AugAssign(self, node: Assign) -> Any:
        self.sstmt_lst.append(AugAssignStmt(node))
        return node 
    