import ast

class VarsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = list()

    def _ctx2str(self, ctx):
        if isinstance(ctx, ast.Load):
            return "load"
        elif isinstance(ctx, ast.Store):
            return "store"
        elif isinstance(ctx, ast.Del):
            return "del"
        else:
            raise Exception("unknown variable context")

    def visit_Name(self, node):
        var_info = {
                      "name": node.id, 
                      "lineno": node.lineno, 
                      "col_offset": node.col_offset,
                      "usage" : self._ctx2str(node.ctx)
                  }

        self.result.append(var_info)


    def visit_BoolOp(self, node):
        for v in node.values:
            self.visit(v)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.operand)

    def visit_Lambda(self, node):
        return node

    def visit_IfExp(self, node):
        self.visit(node.test)
        self.visit(node.body)
        self.visit(node.orelse)

    def visit_Dict(self, node):
        for k in node.keys:
            if k is not None:
                self.visit(k)
        for v in node.values:
            self.visit(v)

    def visit_Set(self, node):
        for e in node.elts:
            self.visit(e)

    def comprehension(self, node):
        self.visit(node.target)
        self.visit(node.iter)
        for c in node.ifs:
            self.visit(c)

    def visit_ListComp(self, node):
        for gen in node.generators:
            self.comprehension(gen)
        self.visit(node.elt)

    def visit_SetComp(self, node):
        self.visit(node.elt)
        for gen in node.generators:
            self.comprehension(gen)

    def visit_DictComp(self, node):
        for gen in node.generators:
            self.comprehension(gen)
        self.visit(node.key)
        self.visit(node.value)


    def visit_GeneratorComp(self, node):
        self.visit(node.elt)
        for gen in node.generators:
            self.comprehension(gen)

    def visit_Yield(self, node):
        if node.value:
            self.visit(node.value)

    def visit_YieldFrom(self, node):
        self.visit(node.value)

    def visit_Compare(self, node):
        self.visit(node.left)
        for c in node.comparators:
            self.visit(c)

    def visit_Call(self, node):
        self.visit(node.func)
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword)

    def visit_keyword(self, node):
        self.visit(node.value)

    def visit_Attribute(self, node):
        full_name = self.get_attr_name(node)

        var_info = {  
                    "name": full_name, 
                    "lineno": node.lineno, 
                    "col_offset": node.col_offset,
                    "usage" : self._ctx2str(node.ctx)
                }
        self.result.append(var_info)
        self.visit(node.value)

    def get_attr_name (self, node):
        if isinstance(node, ast.Call):
            # to be test
            return self.get_attr_name(node.func)
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            attr_name = self.get_attr_name(node.value)
            if attr_name is None:
                return None
            return attr_name +"."+node.attr
        elif isinstance(node, ast.Subscript):
            return self.get_attr_name(node.value)
        else:
            # such as (a**2).sum()
            return None

    def slicev(self, node):

        if isinstance(node, ast.Constant):
            return 
        if isinstance(node, ast.Slice):
            if node.lower:
                self.visit(node.lower)
            if node.upper:
                self.visit(node.upper)
            if node.step:
                self.visit(node.step)
        elif isinstance(node, ast.ExtSlice):
            if node.dims:
                for d in node.dims:
                    self.visit(d)
        elif isinstance(node,ast.Tuple):
            for elt in node.elts:
                self.visit(elt)
        elif isinstance(node, ast.UnaryOp):
            self.visit(node.operand)
        elif isinstance(node, ast.Name):
            self.visit(node)
        # this is due to syntax change 
        elif hasattr(node, "value"):
            self.visit(node.value)

    def visit_Subscript(self, node):
        if isinstance(node.value, ast.Attribute):
            pass
        self.visit(node.value)
        self.slicev(node.slice)

    def visit_Starred(self, node):
        self.visit(node.value)

    def visit_List(self, node):
        for el in node.elts:
            self.visit(el)

    def visit_Tuple(self, node):
        for el in node.elts:
            self.visit(el)

    def visit_FunctionDef(self, node): 
 
        for stmt in node.body:
            self.visit(stmt)
        #return node

    def visit_Assign(self, node):
        for target in node.targets:
            #if isinstance(target, ast.Subscript):
            #    target.value.ctx = ast.Store()
            self.visit(target)
        if not isinstance(node.value, ast.Lambda):
            self.visit(node.value)

            #for target in node.targets:
            #    if isinstance(target, ast.Subscript):
            #        target.value.ctx = ast.Store()
            #    self.visit(target)
        #else:
        #    self.visit(target)


def get_vars(node):
    visitor = VarsVisitor()
    visitor.visit(node)
    return visitor.result
