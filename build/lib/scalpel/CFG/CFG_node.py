'''
This implementation is adapted from Rahul Gopinath' work and FuzzyBook by  at 
https://rahul.gopinath.org/post/2019/12/08/python-controlflow/

'''
import ast
import re
import astunparse
class CFGNode:
    counter = 0
    registry = {}
    stack = []
    def __init__(self, parents=[], ast=None, label=None, annot=None):
        self.parents = parents
        self.calls = []
        self.children = []
        self.ast_node = ast
        self.label = label
        self.annot = annot
        self.rid  = CFGNode.counter
        CFGNode.registry[self.rid] = self
        CFGNode.counter += 1
    def add_child(self, c):
        if c not in self.children:
            self.children.append(c)

    def add_parent(self, p):
        if p not in self.parents:
            self.parents.append(p)

    def add_parents(self, ps):
        for p in ps:
            self.add_parent(p)

    def add_calls(self, func):
        mid = None
        if hasattr(func, 'id'): # ast.Name
            mid = func.id
        else: # ast.Attribute
            mid = func.value.id
        self.calls.append(mid)
    def __eq__(self, other):
        return self.rid == other.rid

    def __neq__(self, other):
        return self.rid != other.rid

    def lineno(self):
        return self.ast_node.lineno if hasattr(self.ast_node, 'lineno') else 0
        
    def name(self):
        return str(self.rid)
        
    def expr(self):
        return self.source()
        
    def __str__(self):
        return "id:%d line[%d] parents: %s : %s" % \
           (self.rid, self.lineno(), str([p.rid for p in self.parents]), self.source())

    def __repr__(self):
        return str(self)

    def source(self):
        return astunparse.unparse(self.ast_node).strip()

    def annotation(self):
        if self.annot is not None:
            return self.annot
        return self.source()

    def to_json(self):
        return {'id':self.rid, 'parents': [p.rid for p in self.parents],
               'children': [c.rid for c in self.children],
               'calls': self.calls, 'at':self.lineno() ,'ast':self.source()}
    def get_gparent_id(self):
        p = CFGNode.registry[self.rid]
        while not p.annotation():
            p = p.parents[0]
        return str(p.rid)
