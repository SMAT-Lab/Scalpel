import ast 
from stmt.stmt import StmtVisitor


code_src = """

# class ast.FunctionDef(name, args, body, decorator_list, returns, type_comment)
# class ast.AsyncFunctionDef(name, args, body, decorator_list, returns, type_comment)
# class ast.ClassDef(name, bases, keywords, body, decorator_list)
# class ast.Return(value)

class Foo(base1, base2, metaclass=meta):
    def foo(self):
        return 4

# class ast.Delete(targets)
del x,y,z


# class ast.Assign(targets, value, type_comment)

a = b = 1

a,b = c


# class ast.AugAssign(target, op, value)

x += 2


# class ast.AnnAssign(target, annotation, value, simple)

c: int

(a): int = 1

a.b: int

a[1]: int


# class ast.For(target, iter, body, orelse, type_comment)

for x in y:
    ...
else:
    ...


# class ast.With(items, body, type_comment)

with a as b, c as d:
   something(b, d)


# class ast.AsyncFor(target, iter, body, orelse, type_comment)
# class ast.AsyncWith(items, body, type_comment)
# class ast.While(test, body, orelse)

while x:
    ...
else:
    ...


# class ast.If(test, body, orelse)
if x:
    ...
elif y:
    ...
else:
    ...

# class ast.Match(subject, cases)
match x:
    case 1 if x>0:
        ... 
    case tuple():
        ... 



# class ast.MatchValue(value)
match x:
    case "Relevant":
        ...


# class ast.MatchSingleton(value)
match x:
    case None:
        ...


# class ast.MatchSequence(patterns)
match x:
    case [1, 2]:
        ...


# class ast.MatchStar(name)
match x:
    case [1, 2, *rest]:
        ...
    case [*_]:
        ...


# class ast.MatchMapping(keys, patterns, rest)
match x:
    case {1: _, 2: _}:
        ...
    case {**rest}:
        ...


# class ast.MatchClass(cls, patterns, kwd_attrs, kwd_patterns)
match x:
    case Point2D(0, 0):
        ...
    case Point3D(x=0, y=0, z=0):
        ...


# class ast.MatchAs(pattern, name)
match x:
    case [x] as y:
        ...
    case _:
        ...


# class ast.MatchOr(patterns)
match x:
    case [x] | (y):
        ...


# class ast.Raise(exc, cause)
raise x from y

# class ast.Try(body, handlers, orelse, finalbody)
try:
   ...
except Exception:
   ...
except OtherException as e:
   ...
else:
   ...
finally:
   ...


# class ast.TryStar(body, handlers, orelse, finalbody)
# only for python3.10
#try:
#    ...
#except* Exception:
#    ...


# class ast.Assert(test, msg)
assert x,y


# class ast.Import(names)
import x,y,z


# class ast.ImportFrom(module, names, level)
from y import x,y,z


# class ast.alias(name, asname)
from ..foo.bar import a as b, c

# class ast.Global(names)
#class ast.Nonlocal(names)

global x,y,z

nonlocal x,y,z


# class ast.Expr(value)
-a

# class ast.Pass
# class ast.Break
# class ast.Continue
for a in b:
    if a > 5:
        break
    else:
        continue
    pass
"""
    
if __name__ == "__main__":
    ast_node = ast.parse(code_src)
    stmt_visitor = StmtVisitor()
    stmt_visitor.visit(ast_node)
    