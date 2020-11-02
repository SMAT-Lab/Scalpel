import ast
class VarsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = list()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.result += [(node.id, "load")]
        if isinstance(node.ctx, ast.Store):
            self.result += [(node.id, "store")]

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
        if not isinstance(node.func, ast.Name) and not isinstance(node.func, ast.Call) and not isinstance(node.func, ast.Lambda):
            self.visit(node.func.value)
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword)

    def visit_keyword(self, node):
        self.visit(node.value)

    def visit_Attribute(self, node):
        if not isinstance(node.value, ast.Name):
            self.visit(node.value)
        else:
            if isinstance(node.value.ctx, ast.Load):
                self.result.append((node.value.id, 'load'))
            else:
                self.result.append((node.value.id, 'store'))

    def slicev(self, node):
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
        else:
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

    def visit_FunctionDef(self_r, node):
        return node

    def visit_Assign(self, node):
        if not isinstance(node.value, ast.Lambda):
            self.visit(node.value)
            for target in node.targets:
                if isinstance(target, ast.Subscript):
                    target.value.ctx = ast.Store()
                self.visit(target)

def get_vars(node):
    visitor = VarsVisitor()
    visitor.visit(node)
    return visitor.result
