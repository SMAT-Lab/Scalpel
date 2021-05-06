'''
This implementation is adapted from Rahul Gopinath' work and fuzzybook:
https://rahul.gopinath.org/post/2019/12/08/python-controlflow/
https://www.fuzzingbook.org/html/ControlFlow.html

'''
import ast
import re
import astunparse
from .CFGNode import *

DEFS_HAVE_PARENTS = False


class CFGExtractor:
    def __init__(self):
        self.founder = CFGNode(parents=[], ast=ast.parse('start').body[0]) # sentinel
        self.founder.ast_node.lineno = 0
        self.functions = {}
        self.functions_node = {}

    def walk(self, node, myparents):
        if node is None: return
        fname = "on_%s" % node.__class__.__name__.lower()
        if hasattr(self, fname):
            return getattr(self, fname)(node, myparents)
        raise SyntaxError('walk: Not Implemented in %s' % type(node))

    def on_pass(self, node, myparents):
        p = [CFGNode(parents=myparents, ast=node)]
        return p

    def on_module(self, node, myparents):
        p = myparents
        for n in node.body:
            p = self.walk(n, p)
        return p

    def on_str(self, node, myparents):
        p = [CFGNode(parents=myparents, ast=node, annot='')]
        return p

    def on_num(self, node, myparents):
        p = [CFGNode(parents=myparents, ast=node, annot='')]
        return p
    def on_expr(self, node, myparents):
        p = self.walk(node.value, myparents)
        p = [CFGNode(parents=p, ast=node)]
        return p

    def on_unaryop(self, node, myparents):
        p = [CFGNode(parents=myparents, ast=node, annot='')]
        return self.walk(node.operand, p)

    def on_binop(self, node, myparents):
        left = self.walk(node.left, myparents)
        right = self.walk(node.right, left)
        p = [CFGNode(parents=right, ast=node, annot='')]
        return p

    def on_compare(self, node, myparents):
        left = self.walk(node.left, myparents)
        right = self.walk(node.comparators[0], left)
        p = [CFGNode(parents=right, ast=node, annot='')]
        return p

    def on_assign(self, node, myparents):
        if len(node.targets) > 1: raise NotImplemented('Parallel assignments')
        p = [CFGNode(parents=myparents, ast=node)]
        p = self.walk(node.value, p)
        return p

    def on_name(self, node, myparents):
        p = [CFGNode(parents=myparents, ast=node, annot='')]
        return p

    def on_if(self, node, myparents):
        p = self.walk(node.test, myparents)
        test_node = [CFGNode(parents=p, ast=node, annot="if: %s" % astunparse.unparse(node.test).strip())]
        g1 = test_node
        g_true = [CFGNode(parents=g1, ast=None, label="if:True", annot='')]
        g1 = g_true
        for n in node.body:
            g1 = self.walk(n, g1)
        g2 = test_node
        g_false = [CFGNode(parents=g2, ast=None, label="if:False", annot='')]
        g2 = g_false
        for n in node.orelse:
            g2 = self.walk(n, g2)
        return g1 + g2

    def on_while(self, node, myparents):
        loop_id = CFGNode.counter
        lbl1_node = CFGNode(parents=myparents, ast=node, label='loop_entry', annot='%s:while' % loop_id)
        p = self.walk(node.test, [lbl1_node])

        lbl2_node = CFGNode(parents=p, ast=node.test, label='while:test', annot='if: %s' % astunparse.unparse(node.test).strip())
        g_false = CFGNode(parents=[lbl2_node], ast=None, label="if:False", annot='')
        g_true = CFGNode(parents=[lbl2_node], ast=None, label="if:True", annot='')
        lbl1_node.exit_nodes = [g_false]
        p = [g_true]

        for n in node.body:
            p = self.walk(n, p)
        # the last node is the parent for the lb1 node.
        lbl1_node.add_parents(p)

        return lbl1_node.exit_nodes

    def on_break(self, node, myparents):
        parent = myparents[0]
        while parent.label != 'loop_entry':
            parent = parent.parents[0]

        assert hasattr(parent, 'exit_nodes')
        p = CFGNode(parents=myparents, ast=node)

        # make the break one of the parents of label node.
        parent.exit_nodes.append(p)

        # break doesnt have immediate children
        return []

    def on_continue(self, node, myparents):
        parent = myparents[0]
        while parent.label != 'loop_entry':
            parent = parent.parents[0]
        p = CFGNode(parents=myparents, ast=node)
        parent.add_parent(p)
        return []

    def on_call(self, node, myparents):
        p = myparents
        for a in node.args:
            p = self.walk(a, p)
        myparents[0].add_calls(node.func)
        p = [CFGNode(parents=p, ast=node, label='call', annot='')]
        return p

    def on_for(self, node, myparents):
        #node.target in node.iter: node.body
        loop_id = CFGNode.counter

        for_pre = CFGNode(parents=myparents, ast=None, label='for_pre', annot='')

        init_node = ast.parse('__iv_%d = iter(%s)' % (loop_id, astunparse.unparse(node.iter).strip())).body[0]
        p = self.walk(init_node, [for_pre])

        lbl1_node = CFGNode(parents=p, ast=node, label='loop_entry', annot='%s: for' % loop_id)
        _test_node = ast.parse('__iv_%d.__length__hint__() > 0' % loop_id).body[0].value
        p = self.walk(_test_node, [lbl1_node])

        lbl2_node = CFGNode(parents=p, ast=_test_node, label='for:test', annot='for: %s' % astunparse.unparse(_test_node).strip())
        g_false = CFGNode(parents=[lbl2_node], ast=None, label="if:False", annot='')
        g_true = CFGNode(parents=[lbl2_node], ast=None, label="if:True", annot='')
        lbl1_node.exit_nodes = [g_false]

        p = [g_true]

        # now we evaluate the body, one at a time.
        for n in node.body:
            p = self.walk(n, p)

        # the test node is looped back at the end of processing.
        lbl1_node.add_parents(p)

        return lbl1_node.exit_nodes


    def on_functiondef(self, node, myparents):
        # name, args, body, decorator_list, returns
        fname = node.name
        args = node.args
        returns = node.returns
        p = myparents if DEFS_HAVE_PARENTS else []

        enter_node = CFGNode(parents=p, ast=node, label='enter', annot='<define>: %s' % node.name)
        enter_node.return_nodes = [] # sentinel

        p = [enter_node]
        for n in node.body:
            p = self.walk(n, p)

        enter_node.return_nodes.extend(p)

        self.functions[fname] = [enter_node, enter_node.return_nodes]
        self.functions_node[enter_node.lineno()] = fname

        return myparents

    def on_return(self, node, myparents):
        parent = myparents[0]

        val_node = self.walk(node.value, myparents)
        # on return look back to the function definition.
        while not hasattr(parent, 'return_nodes'):
            parent = parent.parents[0]
        assert hasattr(parent, 'return_nodes')
        p = CFGNode(parents=val_node, ast=node)
        # make the break one of the parents of label node.
        parent.return_nodes.append(p)
        # return doesnt have immediate children
        return []
    def parse(self, src):
        return ast.parse(src)
    def gen_cfg(self, src):
        node = self.parse(src)
        nodes = self.walk(node, [self.founder])
        self.last_node = CFGNode(parents=nodes, ast=ast.parse('stop').body[0])
