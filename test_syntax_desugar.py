import os
import sys
import ast
import astor
from scalpel.core.module_graph import MNode, ModuleGraph, UnitWalker
from scalpel.rewriter import Rewriter
from scalpel.SSA.ssa import SSA

def listcomp2loop(comp_node, target_name):
    iter = comp_node.generators[0].iter
    ifs  = comp_node.generators[0].ifs
    target = comp_node.generators[0].target
    orelse = []
    new_lst_name = "_hidden_" + target_name
    def_target = ast.Name(id=new_lst_name, ctx=ast.Store()) 
    new_lst_def = ast.Assign([def_target], ast.List([], ast.Load()))
    if len(ifs) == 0:
        append_attr = ast.Attribute(value=ast.Name(id=new_lst_name, ctx=ast.Load()),attr='append', ctx=ast.Load())
        append_call = ast.Call(append_attr, [comp_node.elt], [])
        append_stmt = ast.Expr(append_call)
        body_stmts = [append_stmt]
    else:
        append_attr = ast.Attribute(value=ast.Name(id=new_lst_name, ctx=ast.Load()),attr='append', ctx=ast.Load())
        append_call = ast.Call(append_attr, [comp_node.elt], [])
        append_stmt = ast.Expr(append_call)
        if_body_stmts = [append_stmt]
        if_stmt = ast.If(ifs[0], if_body_stmts, [])
        body_stmts = [if_stmt]
        pass
    return [new_lst_def, ast.For(target, iter, body_stmts, orelse)]

def rewrite(node):
    if isinstance(node, ast.Assign): 
        if len(node.targets) ==1 and isinstance(node.value, ast.Subscript):
            if isinstance(node.value.value, ast.ListComp):
                loop_stmts = listcomp2loop(node.value.value, node.targets[0].id)
                new_obj_name = ast.Name(id = "_hidden_"+ str(node.targets[0].id), ctx=ast.Load())
                recover_assignment = ast.Assign(node.targets, ast.Subscript(new_obj_name, node.value.slice))
                loop_stmts.append(recover_assignment)
                return loop_stmts
                pass
        if len(node.targets) ==1 and isinstance(node.value, ast.Lambda):
            if isinstance(node.targets[0], ast.Name):
                fun_name = node.targets[0].id
                return_stmt = ast.Return(node.value.body)
                body_stmts = [return_stmt]
                decorator_list = []
                return [ast.FunctionDef(fun_name, node.value.args, body_stmts,
                    decorator_list)]

        if len(node.targets) ==1 and not isinstance(node.targets[0], ast.Tuple) and isinstance(node.value, ast.ListComp):
            iter = node.value.generators[0].iter
            ifs  = node.value.generators[0].ifs
            #print(ast.dump(node))
            #print(astor.to_source(node))
            #target_name = node.value.generators[0].target.id
            #target = ast.Name(id=node.targets[0].id, ctx=ast.Store())
            target = node.value.generators[0].target
            orelse = []
            #src = astor.to_source(node)
            #print(src)
            # X, Y = [cbook.safe_masked_invalid(a) for a in args[:2]]
            #new_lst_name = "_hidden_" + node.targets[0].id

            #if instance(node.targets[0])
            #def_target = ast.Name(id=new_lst_name, ctx=ast.Store()) 
            new_lst_def = ast.Assign(node.targets, ast.List([], ast.Load()))
            #new_lst_def = ast.Assign([def_target], ast.List([], ast.Load()))

            #recover_assignment = ast.Assign(node.targets, ast.Name(id=new_lst_name, ctx=ast.Load()))

            if len(ifs) == 0:
                #append_attr = ast.Attribute(value=ast.Name(id=new_lst_name, ctx=ast.Load()),attr='append', ctx=ast.Load())
                append_attr = ast.Attribute(value=node.targets[0],attr='append', ctx=ast.Load())
                append_call = ast.Call(append_attr, [node.value.elt], [])
                append_stmt = ast.Expr(append_call)
                body_stmts = [append_stmt]
            else:
                append_attr = ast.Attribute(value= node.targets[0],attr='append', ctx=ast.Load())
                append_call = ast.Call(append_attr, [node.value.elt], [])
                append_stmt = ast.Expr(append_call)
                if_body_stmts = [append_stmt]
                if_stmt = ast.If(ifs[0], if_body_stmts, [])
                body_stmts = [if_stmt]
                pass
            #return [new_lst_def, ast.For(target, iter, body_stmts, orelse), recover_assignment]
            return [new_lst_def, ast.For(target, iter, body_stmts, orelse)]
        if isinstance(node.value, ast.Call):
            new_stmts = []
            n_args = len(node.value.args)
            for i in range(n_args):
                if isinstance(node.value.args[i], ast.Call):
                    res_name = "_hidden_res_{}_{}".format(node.value.args[i].lineno, node.value.args[i].col_offset)
                    res_name_obj = ast.Name(id=res_name, ctx = ast.Store())
                    assign_tmp = ast.Assign([res_name_obj], node.value.args[i])
                    res_name_obj.ctx = ast.Load()
                    node.value.args[i] = res_name_obj
                    new_stmts.append(assign_tmp)
                elif isinstance(node.value.args[i], ast.ListComp):
                    res_name = "_hidden_res_{}_{}".format(node.value.args[i].lineno, node.value.args[i].col_offset)
                    res_name_obj = ast.Name(id=res_name, ctx = ast.Store())
                    assign_tmp = ast.Assign([res_name_obj], node.value.args[i])
                    arg_node = node.value.args[i]
                    iter = arg_node.generators[0].iter
                    ifs  = arg_node.generators[0].ifs
                    target = arg_node.generators[0].target
                    orelse = []

                    res_lst_name = "_hidden_res_{}_{}".format(node.value.args[i].lineno, node.value.args[i].col_offset)
                    def_target = ast.Name(id=res_lst_name, ctx=ast.Store()) 
                    new_lst_def = ast.Assign([def_target], ast.List([], ast.Load()))
                    if len(ifs) == 0:
                        append_attr = ast.Attribute(value=ast.Name(id=res_lst_name, ctx=ast.Load()),attr='append', ctx=ast.Load())
                        append_call = ast.Call(append_attr, [arg_node.elt], [])
                        append_stmt = ast.Expr(append_call)
                        body_stmts = [append_stmt]
                    else:
                        append_attr = ast.Attribute(value=ast.Name(id=res_lst_name, ctx=ast.Load()),attr='append', ctx=ast.Load())
                        append_call = ast.Call(append_attr, [arg_node.elt], [])
                        append_stmt = ast.Expr(append_call)
                        if_body_stmts = [append_stmt]
                        if_stmt = ast.If(ifs[0], if_body_stmts, [])
                        body_stmts = [if_stmt]
                    res_name_obj.ctx = ast.Load()
                    node.value.args[i] = res_name_obj
                    arg_new_stmts = [new_lst_def, ast.For(target, iter,
                        body_stmts, orelse)]
                    new_stmts.extend(arg_new_stmts)
            new_stmts.append(node)

            return new_stmts


    return [node]

def test_syntax_desugar():
    filename = sys.argv[1]
    source = open(filename).read()

    module_node = ast.parse(source)
    Walker = UnitWalker(module_node)
    for unit in Walker:
        new_stmts = rewrite(unit.node)
        unit.insert_stmts_before(new_stmts)
        pass
        #unit.insert_before()
    #rewriter = Rewriter(source)
    #new_ast = rewriter.rewrite()
    new_ast = ast.fix_missing_locations(module_node)
    new_src = astor.to_source(new_ast)
    #print(source)
    #print('---------------------------')
    print(new_src)

if __name__ == '__main__':
    test_syntax_desugar()
