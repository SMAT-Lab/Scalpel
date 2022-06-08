""" 
The objective of rewriting module of Scalple is to provide APIs that allow users to rewrite their code implenmentation. 
This can be used for various purposes such as code desugaring (removing code sugar usages), testing and code instrumentation.
Code rewriting can bring great benefits such as API extraction and dynamic testing.
"""

import os
import sys
import ast
import random 
import astor
from astor.source_repr import count  

from scalpel.core.util import  UnitWalker
from scalpel.core.vars_visitor import get_vars



class Rewriter:
    """
    The rewriter class contains a set of static methods. 
    """
    def __init__(self, src):
        self.src = src
        self.ast = ast.parse(src)
        
    @staticmethod
    def rewrite(src, rule_func= None):
        """
        To constuct a import graph.
        Args:
        src: the source code to be rewritten
        rule_func: the function that should be applied for each of statements. 
        The value of rule_func must not be None
        """
        if rule_func is None:
            raise Exception("rule_func cannot be None type!")

        module_node = ast.parse(src)
        Walker = UnitWalker(module_node)
        for unit in Walker:
            new_stmts = rule_func(unit.node)
            if not isinstance(new_stmts, list):
                raise Exception("The return type for rule_func function must be list type!")
            unit.insert_stmts_before(new_stmts)

        new_ast = ast.fix_missing_locations(module_node)
        new_src = astor.to_source(new_ast)
        return new_src 

    def random_var_renaming(self, new_name_candidates = [], K = 2):
        
        all_vars = get_vars(self.ast, skip_call_name=True)

        var_name_set = [var["name"] for var in all_vars if "." not in var["name"] ]
        if K>len(var_name_set):
            raise Exception("K is too large for given input")   
             
        if K>len(new_name_candidates):
            raise Exception("K is too large for given new name candidates")   
            
        chosen_vars = random.sample(var_name_set, K)
        chosen_new_names = random.sample(new_name_candidates, K)
        renaming_pairs = zip(chosen_vars, chosen_new_names)
        
        
        renaming_dict = dict(renaming_pairs)
        
        renamer = VarRenamer(renaming_dict)
        
        self.ast = renamer.visit(self.ast)
        
        self.ast = ast.fix_missing_locations(self.ast)

    def unused_stmt_insertion(self):    
        inserted_stmt = ast.Expr(ast.Call(ast.Name("print", ast.Load()), [ast.Constant("this is an unused statement")], []))
       
        num_insertion_point = 0
        walker = UnitWalker(self.ast)
        for unit in walker:
            num_insertion_point += 1
        insertion_loc = random.randint(0, num_insertion_point-1)
        idx = 0
        walker = UnitWalker(self.ast)
        for unit in walker: 
            if idx == insertion_loc:
                unit.insert_stmts_before([inserted_stmt, unit.node])
            
            idx += 1
        self.ast = ast.fix_missing_locations(self.ast)
    
    def for2while(self, node):
        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            iter_object = ast.Name("_iter_obj_"+str(node.lineno), ast.Store())
            counter_var = ast.Name("_counter_"+str(node.lineno), ast.Store())
            max_counter_var = ast.Name("_len_of_iter_" +str(node.lineno), ast.Store())

            iter_save_stmt = ast.Assign([iter_object], node.iter)
            counter_init_stmt = ast.Assign([counter_var], ast.Constant(0))
            max_counter_init_stmt = ast.Assign([max_counter_var], ast.Call(ast.Name("len"), [iter_object], []))
            test_node = ast.Compare(counter_var, [ast.Lt()], [max_counter_var]) 
            counter_inc_stmt = ast.AugAssign(counter_var, ast.Add(), ast.Constant(1))

            new_target_var =  ast.Subscript(iter_object,counter_var, ast.Load())

            #print(astor.to_source(iter_save_stmt))
            #print(astor.to_source(counter_init_stmt))
            #print(astor.to_source(max_counter_init_stmt))
            #print(astor.to_source(test_node))
            
            new_body = node.body+[counter_inc_stmt]
            while_node = ast.While(test_node, new_body, node.orelse)
            renaming_dict = {node.target.id: new_target_var}
            renamer = VarRenamer(renaming_dict)
            while_node = renamer.visit(while_node)

            return [iter_save_stmt, counter_init_stmt, max_counter_init_stmt, while_node]
        raise Exception("Invalid Input!")
        return node

    def loop_exchange(self):
        Walker = UnitWalker(self.ast)
        for unit in Walker:
            if isinstance(unit.node, ast.For):
                new_stmts = self.for2while(unit.node) 
                unit.insert_stmts_before(new_stmts)

        self.ast = ast.fix_missing_locations(self.ast)
    
    def get_src(self):
        return astor.to_source(self.ast)
        
        
class VarRenamer(ast.NodeTransformer):
    """
    Here is the implementation of code rewriter at AST node level.
    """
  
    def __init__(self, renaming_dict, inserted_node =None):
        self.renaming_dict = renaming_dict
        self.inserted_node = inserted_node 
    
    def visit_Name(self, node):
        if node.id in self.renaming_dict:
            #if type(self.renaming_dict[node.id]) == ast.expr:
            #    print("testing")
            
            target = self.renaming_dict[node.id]
            if type(target) == str:
                node.id = target 
                return node 
            return target 

        return node 
        
    def visit_arg(self, node):
        if node.arg in self.renaming_dict:
            node.arg = self.renaming_dict[node.arg]
        self.generic_visit(node)
        return node
        

class LoopExchanger(ast.NodeTransformer):
    """
    Here is the implementation of code rewriter at AST node level.
    """
    def visit_For(self, node):
        # let something to be assigned by node.iter
        iter_var = ast.Assign()
        # copy the body
        # get the test 
        #make a test
        #new_while_node = ast.While(node.test, node.body, node.orelse)

        return node

   

class ASTRewriter(ast.NodeTransformer):
    """
    Here is the implementation of code rewriter at AST node level.
    """
  
    def __init__(self, src):
  
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
        #if node.id in self.pattern['Name']:
        #    new_name = self.pattern['Name'][node.id]
        #    node.id = new_name
        return node

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
        #if func_name in self.pattern["Call"]:
        #    new_func_name = self.pattern["Call"][func_name]
        #    if new_func_name is None:
        #        return None
        #    node.func.id = new_func_name


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
        # to rewrite

        if len(node.targets) ==1 and isinstance(node.value, ast.Lambda):
            if isinstance(node.targets[0], ast.Name):
                fun_name = node.targets[0].id
                return_stmt = ast.Return(node.value.body)
                body_stmts = [return_stmt]
                decorator_list = []
                return ast.FunctionDef(fun_name, node.value.args, body_stmts, decorator_list)

        if len(node.targets) ==1 and isinstance(node.value, ast.ListComp):
        
            iter = node.value.generators[0].iter
            ifs  = node.value.generators[0].ifs
            target_name = node.value.generators[0].target.id
            target = ast.Name(id=target_name, ctx=ast.Store())

            orelse = []
            new_lst_name = "_hidden_" + node.targets[0].id
            if len(ifs) == 0:
                append_attr = ast.Attribute(value=ast.Name(id=new_lst_name, ctx=ast.Load()),attr='append', ctx=ast.Load())  
                append_call = ast.Call(append_attr, [node.value.elt], [])
                append_stmt = ast.Expr(append_call)
                body_stmts = [append_stmt]
            else:
                append_attr = ast.Attribute(value=ast.Name(id=new_lst_name, ctx=ast.Load()),attr='append', ctx=ast.Load())  
                append_call = ast.Call(append_attr, [node.value.elt], [])
                append_stmt = ast.Expr(append_call)
                if_body_stmts = [append_stmt]
                if_stmt = ast.If(ifs[0], if_body_stmts, [])
                body_stmts = [if_stmt]
                pass
            return ast.For(target, iter, body_stmts, orelse)
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
        #if "if" in self.pattern["Stmt"]:
        #    alt_stmt = self.pattern["Stmt"]["if"]
        #    if alt_stmt is None:
        #        return None

        self.generic_visit(node)

        return node
    def visit_IfExp(self, node): 
        #if "if" in self.pattern["Stmt"]:
        #    alt_stmt = self.pattern["Stmt"]["if"]
        #    if alt_stmt is None:
        #        return None
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

