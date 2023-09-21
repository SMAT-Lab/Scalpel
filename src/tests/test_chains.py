from contextlib import contextmanager
from unittest import TestCase, skipIf
import unittest
import gast as ast
import scalpel.duc as beniget
import io
import sys

# Show full diff in unittest
unittest.util._MAX_LENGTH=2000

@contextmanager
def captured_output():
    if sys.version_info.major >= 3:
        new_out, new_err = io.StringIO(), io.StringIO()
    else:
        new_out, new_err = io.BytesIO(), io.BytesIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestDefUseChains(TestCase):
    def checkChains(self, code, ref, strict=True):



        class StrictDefUseChains(beniget.DefUseChains):
            def warn(self, msg, node):
                raise RuntimeError(f"W: {msg} at {node.lineno}:{node.col_offset}")


        node = ast.parse(code)
        if strict:
            c = StrictDefUseChains()
        else:
            c = beniget.DefUseChains()
        c.visit(node)
        self.assertEqual(c.dump_chains(node), ref)
        return node, c

    def test_simple_expression(self):
        code = "a = 1; a + 2"
        self.checkChains(code, ["a -> (a -> (BinOp -> ()))"])

    def test_expression_chain(self):
        code = "a = 1; (- a + 2) > 0"
        self.checkChains(code, ["a -> (a -> (UnaryOp -> (BinOp -> (Compare -> ()))))"])

    def test_ifexp_chain(self):
        code = "a = 1; a + 1 if a else - a"
        self.checkChains(
            code,
            [
                "a -> ("
                "a -> (IfExp -> ()), "
                "a -> (BinOp -> (IfExp -> ())), "
                "a -> (UnaryOp -> (IfExp -> ()))"
                ")"
            ],
        )

    def test_type_destructuring_tuple(self):
        code = "a, b = range(2); a"
        self.checkChains(code, ["a -> (a -> ())", "b -> ()"])

    def test_type_destructuring_list(self):
        code = "[a, b] = range(2); a"
        self.checkChains(code, ["a -> (a -> ())", "b -> ()"])

    def test_type_destructuring_for(self):
        code = "for a, b in ((1,2), (3,4)): a"
        self.checkChains(code, ["a -> (a -> ())", "b -> ()"])

    if sys.version_info.major >= 3:
        def test_type_destructuring_starred(self):
            code = "a, *b = range(2); b"
            self.checkChains(code, ['a -> ()', 'b -> (b -> ())'])

    def test_assign_in_loop(self):
        code = "a = 2\nwhile 1: a = 1\na"
        self.checkChains(code, ["a -> (a -> ())", "a -> (a -> ())"])

    def test_reassign_in_loop(self):
        code = "m = 1\nfor i in [1, 2]:\n m = m + 1"
        self.checkChains(
            code, ["m -> (m -> (BinOp -> ()))", "i -> ()", "m -> (m -> (BinOp -> ()))"]
        )

    def test_continue_in_loop(self):
        code = "for i in [1, 2]:\n if i: m = 1; continue\n m = 1\nm"
        self.checkChains(
            code, ['i -> (i -> ())', 'm -> (m -> ())', 'm -> (m -> ())']
        )

    def test_break_in_loop(self):
        code = "for i in [1, 2]:\n if i: m = 1; continue\n m = 1\nm"
        self.checkChains(
            code, ['i -> (i -> ())', 'm -> (m -> ())', 'm -> (m -> ())']
        )

    def test_augassign(self):
        code = "a = 1; a += 2; a"
        self.checkChains(code, ['a -> (a -> (a -> ()))'])

    def test_read_global_from_branch(self):
        code = "if 1: a = 1\ndef foo():\n def bar(): global a; return a"
        self.checkChains(code, ['a -> (a -> ())',
                                'foo -> ()'])


    def test_expanded_augassign(self):
        code = "a = 1; a = a + 2"
        self.checkChains(code, ["a -> (a -> (BinOp -> ()))", "a -> ()"])

    def test_augassign_in_loop(self):
        code = "a = 1\nfor i in [1]:\n a += 2\na"
        self.checkChains(code, ['a -> (a -> ((#1), a -> ()), a -> ())',
                                'i -> ()'])

    def test_assign_in_while_in_conditional(self):
        code = """
G = 1
while 1:
    if 1:
        G = 1
    G"""
        self.checkChains(code, ['G -> (G -> ())',
                                'G -> (G -> ())'])

    def test_assign_in_loop_in_conditional(self):
        code = """
G = 1
for _ in [1]:
    if 1:
        G = 1
    G"""
        self.checkChains(code, ['G -> (G -> ())',
                                '_ -> ()',
                                'G -> (G -> ())'])

    def test_simple_print(self):
        code = "a = 1; print(a)"
        if sys.version_info.major >= 3:
            self.checkChains(code, ["a -> (a -> (Call -> ()))"])
        else:
            self.checkChains(code, ["a -> (a -> ())"])

    def test_simple_redefinition(self):
        code = "a = 1; a + 2; a = 3; +a"
        self.checkChains(
            code, ["a -> (a -> (BinOp -> ()))", "a -> (a -> (UnaryOp -> ()))"]
        )

    def test_simple_for(self):
        code = "for i in [1,2,3]: j = i"
        self.checkChains(code, ["i -> (i -> ())", "j -> ()"])

    def test_simple_for_orelse(self):
        code = "for i in [1,2,3]: pass\nelse: i = 4\ni"
        self.checkChains(
            code,
            [
                # assign in loop iteration
                "i -> (i -> ())",
                # assign in orelse
                "i -> (i -> ())",
            ],
        )

    def test_for_break(self):
        code = "i = 8\nfor i in [1,2]:\n break\n i = 3\ni"
        self.checkChains(
            code,
            ['i -> (i -> ())',
             'i -> (i -> ())',
             'i -> ()'])

    def test_for_pass(self):
        code = "i = 8\nfor i in []:\n pass\ni"
        self.checkChains(
            code,
            ['i -> (i -> ())',
             'i -> (i -> ())'])

    def test_complex_for_orelse(self):
        code = "I = J = 0\nfor i in [1,2]:\n if i < 3: I = i\nelse:\n if 1: J = I\nJ"
        self.checkChains(
            code,
            ['I -> (I -> ())',
             'J -> (J -> ())',
             'i -> (i -> (Compare -> ()), i -> ())',
             'I -> (I -> ())',
             'J -> (J -> ())']
        )

    def test_simple_while(self):
        code = "i = 2\nwhile i: i = i - 1\ni"
        self.checkChains(
            code,
            [
                # first assign, out of loop
                "i -> (i -> (), i -> (BinOp -> ()), i -> ())",
                # second assign, in loop
                "i -> (i -> (), i -> (BinOp -> ()), i -> ())",
            ],
        )

    def test_while_break(self):
        code = "i = 8\nwhile 1:\n break\n i = 3\ni"
        self.checkChains(
            code,
            ['i -> (i -> ())',
             'i -> ()'])

    def test_while_cond_break(self):
        code = "i = 8\nwhile 1:\n if i: i=1;break\ni"
        self.checkChains(
            code,
            ['i -> (i -> (), i -> ())', 'i -> (i -> ())'])

    def test_straight_raise(self):
        code = "raise next([e for e in [1]])"
        
        if sys.version_info.major >= 3:
            self.checkChains(code, [])
        else:
            self.checkChains(code, ['e -> (e -> (ListComp -> (Call -> ())))'])

    def test_redefinition_in_comp(self):
        code = "[name for name in 'hello']\nfor name in 'hello':name"
        if sys.version_info.major >= 3:
            self.checkChains(
                code,
                ['name -> (name -> ())'])
        else:
            self.checkChains(
                code,
                ['name -> (name -> (ListComp -> ()))', 'name -> (name -> ())'])

    def test_nested_while(self):
        code = '''
done = 1
while done:

    while done:
        if 1:
            done = 1
            break

        if 1:
            break'''


        self.checkChains(
            code,
            ['done -> (done -> (), done -> ())',
             'done -> (done -> (), done -> ())']
            )

    def test_while_cond_continue(self):
        code = "i = 8\nwhile 1:\n if i: i=1;continue\ni"
        self.checkChains(
            code,
            ['i -> (i -> (), i -> ())', 'i -> (i -> (), i -> ())'])

    def test_complex_while_orelse(self):
        code = "I = J = i = 0\nwhile i:\n if i < 3: I = i\nelse:\n if 1: J = I\nJ"
        self.checkChains(
            code,
            [
                "I -> (I -> ())",
                "J -> (J -> ())",
                "i -> (i -> (), i -> (Compare -> ()), i -> ())",
                "J -> (J -> ())",
                "I -> (I -> ())",
            ],
        )

    def test_while_orelse_break(self):
        code = "I = 0\nwhile I:\n if 1: I = 1; break\nelse: I"
        self.checkChains(
            code,
            ['I -> (I -> (), I -> ())',
             'I -> ()'],
        )

    def test_while_nested_break(self):
        code = "i = 8\nwhile i:\n if i: break\n i = 3\ni"
        self.checkChains(
            code,
            ['i -> (i -> (), i -> (), i -> ())',
             'i -> (i -> (), i -> (), i -> ())'])

    def test_if_true_branch(self):
        code = "if 1: i = 0\ni"
        self.checkChains(code, ["i -> (i -> ())"])

    def test_if_false_branch(self):
        code = "if 1: pass\nelse: i = 0\ni"
        self.checkChains(code, ["i -> (i -> ())"])

    def test_if_both_branch(self):
        code = "if 1: i = 1\nelse: i = 0\ni"
        self.checkChains(code, ["i -> (i -> ())"] * 2)

    def test_if_in_loop(self):
        code = "for _ in [0, 1]:\n if _: i = 1\n else: j = i\ni"
        self.checkChains(code, ["_ -> (_ -> ())", "i -> (i -> (), i -> ())", "j -> ()"])

    def test_with_handler(self):
        code = 'with open("/dev/null") as x: pass\nx'
        self.checkChains(code, ["x -> (x -> ())"])

    def test_simple_try(self):
        code = 'try: e = open("/dev/null")\nexcept Exception: pass\ne'
        self.checkChains(code, ["e -> (e -> ())"])

    def test_simple_except(self):
        code = "try: pass\nexcept Exception as e: pass\ne"
        self.checkChains(code, ["e -> (e -> ())"])

    def test_simple_try_except(self):
        code = 'try: f = open("")\nexcept Exception as e: pass\ne;f'
        self.checkChains(code, ["f -> (f -> ())", "e -> (e -> ())"])

    def test_redef_try_except(self):
        code = 'try: f = open("")\nexcept Exception as f: pass\nf'
        self.checkChains(code, ["f -> (f -> ())", "f -> (f -> ())"])

    def test_simple_import(self):
        code = "import x; x"
        self.checkChains(code, ["x -> (x -> ())"])

    def test_simple_import_as(self):
        code = "import x as y; y()"
        self.checkChains(code, ["y -> (y -> (Call -> ()))"])
    
    def test_simple_lambda(self):
        node, c = self.checkChains( "lambda y: True", [])
        self.assertEqual(c.dump_chains(node.body[0].value), ['y -> ()'])
    
    def test_lambda_defaults(self):
        node, c = self.checkChains( "x=y=1;(lambda y, x=x: (True, x, y, z)); x=y=z=2", 
                                   ['x -> (x -> (Lambda -> ()))',
                                    'y -> ()', 
                                    'x -> ()', 
                                    'y -> ()',
                                    'z -> (z -> (Tuple -> (Lambda -> ())))']) 
        self.assertEqual(c.dump_chains(node.body[1].value), [
            'y -> (y -> (Tuple -> (Lambda -> ())))',
            'x -> (x -> (Tuple -> (Lambda -> ())))',
        ])

    def test_multiple_import_as(self):
        code = "import x as y, z; y"
        self.checkChains(code, ["y -> (y -> ())", "z -> ()"])

    def test_import_from(self):
        code = "from  y import x; x"
        self.checkChains(code, ["x -> (x -> ())"])

    def test_import_from_as(self):
        code = "from  y import x as z; z"
        self.checkChains(code, ["z -> (z -> ())"])

    def test_multiple_import_from_as(self):
        code = "from  y import x as z, w; z"
        self.checkChains(code, ["z -> (z -> ())", "w -> ()"])

    def test_method_function_conflict(self):
        code = "def foo():pass\nclass C:\n def foo(self): foo()"
        self.checkChains(code, ["foo -> (foo -> (Call -> ()))", "C -> ()"])

    def test_nested_if(self):
        code = "f = 1\nif 1:\n if 1:pass\n else: f=1\nelse: f = 1\nf"
        self.checkChains(code, ["f -> (f -> ())", "f -> (f -> ())", "f -> (f -> ())"])

    def test_nested_if_else(self):
        code = "f = 1\nif 1: f = 1\nelse:\n if 1:pass\n else: f=1\nf"
        self.checkChains(code, ["f -> (f -> ())", "f -> (f -> ())", "f -> (f -> ())"])

    def test_try_except(self):
        code = "f = 1\ntry: \n len(); f = 2\nexcept: pass\nf"
        self.checkChains(code, ["f -> (f -> ())", "f -> (f -> ())"])

    def test_attr(self):
        code = "import numpy as bar\ndef foo():\n return bar.zeros(2)"
        self.checkChains(
            code, ["bar -> (bar -> (Attribute -> (Call -> ())))", "foo -> ()"]
        )

    def test_class_decorator(self):
        code = "from some import decorator\n@decorator\nclass C:pass"
        self.checkChains(code, ["decorator -> (decorator -> (C -> ()))", "C -> ()"])

    def test_class_base(self):
        code = "class A:pass\nclass B(A):pass"
        self.checkChains(code, ["A -> (A -> (B -> ()))", "B -> ()"])

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_def_used_in_self_default(self):
        code = "def foo(x:foo): return foo"
        c = beniget.DefUseChains()
        node = ast.parse(code)
        c.visit(node)
        self.assertEqual(c.dump_chains(node), ["foo -> (foo -> ())"])

    def test_unbound_class_variable(self):
        code = '''
def middle():
    x = 1
    class mytype(str):
        x = x+1 # <- this triggers NameError: name 'x' is not defined
    return x
        '''
        c = beniget.DefUseChains()
        node = ast.parse(code)
        c.visit(node)
        self.assertEqual(c.dump_chains(node.body[0]), ['x -> (x -> ())', 'mytype -> ()'])

    def test_unbound_class_variable2(self):
        code = '''class A:\n  a = 10\n  def f(self):\n    return a # a is not defined'''
        c = beniget.DefUseChains()
        node = ast.parse(code)
        c.visit(node)
        self.assertEqual(c.dump_chains(node.body[0]), ['a -> ()', 'f -> ()'])

    def test_unbound_class_variable3(self):
        code = '''class A:\n  a = 10\n  class I:\n    b = a + 1 # a is not defined'''
        c = beniget.DefUseChains()
        node = ast.parse(code)
        c.visit(node)
        self.assertEqual(c.dump_chains(node.body[0]), ['a -> ()', 'I -> ()'])

    def test_unbound_class_variable4(self):
        code = '''class A:\n  a = 10\n  f = lambda: a # a is not defined'''
        c = beniget.DefUseChains()
        node = ast.parse(code)
        c.visit(node)
        self.assertEqual(c.dump_chains(node.body[0]), ['a -> ()', 'f -> ()'])

    def test_unbound_class_variable5(self):
        code = '''class A:\n  a = 10\n  b = [a for _ in range(10)]  # a is not defined'''
        c = beniget.DefUseChains()
        node = ast.parse(code)
        c.visit(node)
        if sys.version_info.major >= 3:
            self.assertEqual(c.dump_chains(node.body[0]), ['a -> ()', 'b -> ()'])
        else:
            self.assertEqual(c.dump_chains(node.body[0]),
                             ['a -> (a -> (ListComp -> ()))', '_ -> ()', 'b -> ()'])

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_functiondef_returns(self):
        code = "x = 1\ndef foo() -> x: pass"
        self.checkChains(code, ['x -> (x -> ())', 'foo -> ()'])

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_arg_annotation(self):
        code = "type_ = int\ndef foo(bar: type_): pass"
        self.checkChains(code, ["type_ -> (type_ -> ())", "foo -> ()"])


    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_inner_class(self):

        code = '''
def outer():
    def middle():
        class mytype(str):
            def count(self) -> mytype: # this should trigger unbound identifier
                def c(x) -> mytype(): # this one shouldn't
                    ...
        '''
        c = beniget.DefUseChains()
        node = ast.parse(code)
        c.visit(node)
        self.assertEqual(c.dump_chains(node.body[0].body[0]), ['mytype -> (mytype -> (Call -> ()))'])

    def check_message(self, code, expected_messages, filename=None):
        node = ast.parse(code)
        c = beniget.DefUseChains(filename)
        with captured_output() as (out, err):
            c.visit(node)

        if not out.getvalue():
            produced_messages = []
        else:
            produced_messages = out.getvalue().strip().split("\n")

        self.assertEqual(len(expected_messages), len(produced_messages),
                         produced_messages)
        for expected, produced in zip(expected_messages, produced_messages):
            self.assertIn(expected, produced,
                          "actual message does not contains expected message")

    def test_unbound_identifier_message_format(self):
        code = "foo(1)\nbar(2)"
        self.check_message(code, ["<unknown>:1", "<unknown>:2"])
        self.check_message(code, ["foo.py:1", "foo.py:2"], filename="foo.py")

    def test_unbound_class_variable_reference_message_format(self):
        code = "class A:\n a = 10\n def f(self): return a # a is undef"
        self.check_message(code, ["unbound identifier 'a' at <unknown>:3"])

    def test_no_unbound_local_identifier_in_comp(self):
        code = "a = []; b = [1 for i in a]"
        self.check_message(code, [])

    def test_maybe_unbound_identifier_message_format(self):
        code = "x = 1\ndef foo(): y = x; x = 2"
        self.check_message(code,
                           ["unbound identifier 'x' at <unknown>:2"])

    def test_unbound_local_identifier_in_func(self):
        code = "def A():\n x = 1\n class B: x = x"
        self.check_message(code,
                           ["unbound identifier 'x' at <unknown>:3"])

    @skipIf(sys.version_info < (3, 0), 'Python 3 syntax')
    def test_unbound_local_identifier_in_method(self):
        code = "class A:pass\nclass B:\n def A(self) -> A:pass"
        self.check_message(code, [])

    @skipIf(sys.version_info < (3, 0), 'Python 3 syntax')
    def test_unbound_local_identifier_nonlocal(self):
        code = "def A():\n x = 1\n class B: nonlocal x; x = x"
        self.check_message(code, [])


    def test_assign_uses_class_level_name(self):
        code = '''
visit_Name = object
class Visitor:
    def visit_Name(self, node):pass
    visit_Attribute = visit_Name
'''
        node = ast.parse(code)
        c = beniget.DefUseChains()
        c.visit(node)
        self.assertEqual(c.dump_chains(node), ['visit_Name -> ()',
                                               'Visitor -> ()'])
        self.assertEqual(c.dump_chains(node.body[-1]),
                         ['visit_Name -> (visit_Name -> ())',
                          'visit_Attribute -> ()'])


    def test_base_class_uses_class_level_same_name(self):
            code = '''
class Attr(object):pass
class Visitor:
    class Attr(Attr):pass
    '''
            node = ast.parse(code)
            c = beniget.DefUseChains()
            c.visit(node)
            self.assertEqual(c.dump_chains(node),
                             ['Attr -> (Attr -> (Attr -> ()))',
                              'Visitor -> ()'])
            self.assertEqual(c.dump_chains(node.body[-1]), ['Attr -> ()'])
    
    @skipIf(sys.version_info < (3, 0), 'Python 3 syntax')
    def test_star_assignment(self):
        code = '''
curr, *parts = [1,2,3]
while curr:
    print(curr)
    if parts:
        curr, *parts = parts
    else:
        break
'''
        self.checkChains(code, ['curr -> (curr -> (), curr -> (Call -> ()))', 
                                'parts -> (parts -> (), parts -> ())']*2)
    
    @skipIf(sys.version_info < (3, 0), 'Python 3 syntax')
    def test_star_assignment_nested(self):
        code = '''
(curr, *parts),i = [1,2,3],0
while curr:
    print(curr)
    if parts:
        (curr, *parts),i = parts,i
    else:
        break
'''
        self.checkChains(code, ['curr -> (curr -> (), curr -> (Call -> ()))',
                                'parts -> (parts -> (), parts -> (Tuple -> ()))',
                                'i -> (i -> (Tuple -> ()))']*2)
    
    def test_attribute_assignment(self):
        code = "d=object();d.name,x = 't',1"
        self.checkChains(code, ['d -> (d -> (Attribute -> ()))',
                                'x -> ()'])

    def test_call_assignment(self):
        code = "NameError().name = 't'"
        self.checkChains(code, [])

    @skipIf(sys.version_info < (3, 0), 'Python 3 syntax')
    def test_annotation_uses_class_level_name(self):
        code = '''
Thing = object
def f():...
class Visitor:
    Thing = bytes
    def f(): return f()
    def visit_Name(self, node:Thing, fn:f):...
'''
        node = ast.parse(code)
        c = beniget.DefUseChains()
        c.visit(node)
        self.assertEqual(c.dump_chains(node),
                         ['Thing -> ()',
                          'f -> (f -> (Call -> ()))',
                          'Visitor -> ()'])
        self.assertEqual(c.dump_chains(node.body[-1]),
                         ['Thing -> (Thing -> ())',
                          'f -> (f -> ())',
                          'visit_Name -> ()'])

    def test_assign_uses_class_level_same_name(self):
        code = '''
def visit_Attribute(self, node):pass
class Visitor:
    visit_Attribute = visit_Attribute
'''
        node = ast.parse(code)
        c = beniget.DefUseChains()
        c.visit(node)
        self.assertEqual(c.dump_chains(node),
            ['visit_Attribute -> (visit_Attribute -> ())',
             'Visitor -> ()'])
        self.assertEqual(c.dump_chains(node.body[-1]),
                         ['visit_Attribute -> ()'])

    def test_unbound_local_identifier_in_augassign(self):
        code = "def A():\n x = 1\n class B: x += 1"
        self.check_message(code,
                           ["unbound identifier 'x' at <unknown>:3"])

    def test_star_import_with_conditional_redef(self):
        code = '''
from math import *

if 1:
    def pop():
        cos()
cos = pop()'''
        self.checkChains(code, [
            '* -> (cos -> (Call -> ()))',
            'pop -> (pop -> (Call -> ()))',
            'cos -> (cos -> (Call -> ()))'
        ])
    
    @skipIf(sys.version_info < (3, 0), 'Python 3 semantics')
    def test_class_scope_comprehension(self):
        code = '''
class Cls:
    foo = b'1',
    [_ for _ in foo]
    {_ for _ in foo}
    (_ for _ in foo)
    {_:1 for _ in foo}
'''
        node, chains = self.checkChains(code, ['Cls -> ()'])
        self.assertEqual(chains.dump_chains(node.body[0]),
                         ['foo -> ('
                          'foo -> (comprehension -> (ListComp -> ())), '
                          'foo -> (comprehension -> (SetComp -> ())), '
                          'foo -> (comprehension -> (GeneratorExp -> ())), '
                          'foo -> (comprehension -> (DictComp -> ())))'])
    
    @skipIf(sys.version_info < (3, 0), 'Python 3 semantics')
    def test_class_scope_comprehension_invalid(self):
        code = '''
class Foo:
    x = 5
    y = [x for i in range(1)]
    z = [i for i in range(1) for j in range(x)]
'''
        self.check_message(code, ["W: unbound identifier 'x' at test:4:9", 
                                  "W: unbound identifier 'x' at test:5:44"], 'test')


    @skipIf(sys.version_info < (3, 8), 'Python 3.8 syntax')
    def test_named_expr_simple(self):
        code = '''
if (x := 1):
    y = x + 1'''
        self.checkChains(
            code, ['x -> (x -> (BinOp -> ()))', 'y -> ()']
        )

    @skipIf(sys.version_info < (3, 8), 'Python 3.8 syntax')
    def test_named_expr_complex(self):
        code = '''
if (x := (y := 1) + 1):
    z = x + y'''
        self.checkChains(
            code, ['y -> (y -> (BinOp -> ()))', 'x -> (x -> (BinOp -> ()))', 'z -> ()']
        )

    @skipIf(sys.version_info < (3, 8), 'Python 3.8 syntax')
    def test_named_expr_with_rename(self):
        code = '''
a = 1
if (a := a + a):
    pass'''
        self.checkChains(
            code, ['a -> (a -> (BinOp -> (NamedExpr -> ())), a -> (BinOp -> (NamedExpr -> ())))', 'a -> ()']
        )
    
    @skipIf(sys.version_info < (3, 8), 'Python 3.8 syntax')
    def test_named_expr_comprehension(self):
        # Warlus target should be stored in first non comprehension scope
        code = ('cities = ["Halifax", "Toronto"]\n'
            'if any((witness := city).startswith("H") for city in cities):'
            'witness')
        self.checkChains(
            code, ['cities -> (cities -> (comprehension -> (GeneratorExp -> (Call -> ()))))', 
                   'witness -> (witness -> ())']
        )
        
    @skipIf(sys.version_info < (3, 8), 'Python 3.8 syntax')
    def test_named_expr_comprehension_invalid(self):
        # an assignment expression target name cannot be the same as a 
        # for-target name appearing in any comprehension containing the assignment expression.
        # A further exception applies when an assignment expression occurs in a comprehension whose 
        # containing scope is a class scope. If the rules above were to result in the target 
        # being assigned in that class's scope, the assignment expression is expressly invalid.
        code = '''
stuff = []

# assignment expression cannot rebind comprehension iteration variable
[[(a := a) for _ in range(5)] for a in range(5)] # INVALID
[b := 0 for b, _ in stuff] # INVALID
[c for c in (c := stuff)] # INVALID
[False and (d := 0) for d, _ in stuff] # INVALID
[_ for _, e in stuff if True or (e := 1)] # INVALID

# assignment expression cannot be used in a comprehension iterable expression
[_ for _ in (f := stuff)] # INVALID
[_ for _ in range(2) for _ in (g := stuff)] # INVALID
[_ for _ in [_ for _ in (h := stuff)]] # INVALID
[_ for _ in (lambda: (i := stuff))()] # INVALID

class Example:
    # assignment expression within a comprehension cannot be used in a class body
    [(j := i) for i in range(5)] # INVALID
'''
        # None of the invalid assigned name shows up.
        node, chains = self.checkChains(code, ['stuff -> ()', 'Example -> ()'], strict=False)        
        self.assertEqual(chains.dump_chains(node.body[-1]), [])
        # It triggers useful warnings
        self.check_message(code, ["W: assignment expression cannot rebind comprehension iteration variable 'a' at <unknown>:5:0", 
                                  "W: assignment expression cannot rebind comprehension iteration variable 'b' at <unknown>:6:0", 
                                  'W: assignment expression cannot be used in a comprehension iterable expression at <unknown>:7:0', 
                                  "W: assignment expression cannot rebind comprehension iteration variable 'd' at <unknown>:8:0", 
                                  "W: assignment expression cannot rebind comprehension iteration variable 'e' at <unknown>:9:0", 
                                  'W: assignment expression cannot be used in a comprehension iterable expression at <unknown>:12:0', 
                                  'W: assignment expression cannot be used in a comprehension iterable expression at <unknown>:13:0', 
                                  'W: assignment expression cannot be used in a comprehension iterable expression at <unknown>:14:0', 
                                  'W: assignment expression cannot be used in a comprehension iterable expression at <unknown>:15:0',
                                  'W: assignment expression within a comprehension cannot be used in a class body at <unknown>:19:6'])
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_unbound(self):
        code = '''
def f(x:f) -> f: # 'f' annotations are unbound
    ...'''
        self.checkChains(
            code, ['f -> ()'], strict=False
        )
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_method_annotation_unbound(self):
        code = '''
class S:
    def f(self, x:f) -> f:... # 'f' annotations are unbound
'''
        mod, chains = self.checkChains(
            code, ['S -> ()'], strict=False
        )
        self.assertEqual(chains.dump_chains(mod.body[0]), 
                         ['f -> ()'])
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_unbound_pep563(self):
        code = '''
from __future__ import annotations
def f(x:f) -> f: # 'f' annotations are NOT unbound because pep563
    ...'''
        self.checkChains(
            code, ['annotations -> ()', 'f -> (f -> (), f -> ())']
        )
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_method_annotation_unbound_pep563(self):
        code = '''
from __future__ import annotations
class S:
    def f(self, x:f) -> f:... # 'f' annotations are NOT unbound because pep563
'''
        mod, chains = self.checkChains(
            code, ['annotations -> ()', 'S -> ()']
        )
        self.assertEqual(chains.dump_chains(mod.body[1]), 
                         ['f -> (f -> (), f -> ())'])
    
    def test_import_dotted_name_binds_first_name(self):
        code = '''import collections.abc;collections;collections.abc'''
        self.checkChains(
            code, ['collections -> (collections -> (), collections -> (Attribute -> ()))']
        )

    def test_multiple_wildcards_may_bind(self):
        code = '''from abc import *; from collections import *;name1; from mod import *;name2'''
        self.checkChains(
            code, ['* -> (name1 -> (), name2 -> ())','* -> (name1 -> (), name2 -> ())','* -> (name2 -> ())']
        )
    
    def test_wildcard_may_override(self):
        # we could argue that the wildcard import might override name2,
        # but we're currently ignoring these kind of scenarios.
        code = '''name2=True;from abc import *;name2'''
        self.checkChains(
            code, ['name2 -> (name2 -> ())', '* -> ()']
        )

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_use_upper_scope_variables(self):
        code = '''
from typing import Union
class Attr:
    ...
class Thing:
    ...
class System:
    Thing = bytes
    @property
    def Attr(self) -> Union[Attr, Thing]:...
'''
        self.checkChains(
            code, ['Union -> (Union -> (Subscript -> ()))',
                    'Attr -> (Attr -> (Tuple -> (Subscript -> ())))',
                    'Thing -> ()',
                    'System -> ()',]
        )
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_future_annotation_class_var(self):
        code = '''
from __future__ import annotations
from typing import Type
class System:
    Thing = bytes
    @property
    def Attribute(self) -> Type[Thing]:...
'''     
        
        mod, chains = self.checkChains(
            code, ['annotations -> ()',
            'Type -> (Type -> (Subscript -> ()))', 'System -> ()']
        )
        # locals of System
        self.assertEqual(chains.dump_chains(mod.body[-1]), [
            'Thing -> (Thing -> (Subscript -> ()))', 
            'Attribute -> ()'
        ])
        
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_pep0563_annotations(self):

        # code taken from https://peps.python.org/pep-0563/

        code = '''
# beniget can probably understand this code without the future import
from __future__ import annotations
from typing import TypeAlias, Mapping, Dict, Type
class C:
    
    def method(self) -> C.field:  # this is OK
        ...

    def method(self) -> field:  # this is OK
        ...

    def method(self) -> C.D:  # this is OK
        ...

    def method(self, x:field) -> D:  # this is OK
        ...

    field:TypeAlias = 'Mapping'

    class D:
        field2:TypeAlias = 'Dict'
        def method(self) -> C.D.field2:  # this is OK
            ...

        def method(self) -> D.field2:  # this FAILS, class D is local to C
            ...                        # and is therefore only available
                                       # as C.D. This was already true
                                       # before the PEP. 
                                       # We check first the globals, then the locals
                                       # of the class D, and 'D' is not defined in either
                                       # of those, it defined in the locals of class C.

        def method(self, x:field2) -> field2:  # this is OK
            ...

        def method(self, x) -> field:  # this FAILS, field is local to C and
                                    # is therefore not visible to D unless
                                    # accessed as C.field. This was already
                                    # true before the PEP.
            ...

        def Thing(self, y:Type[Thing]) -> Thing: # this is OK, and it links to the top level Thing.
            ...

Thing:TypeAlias = 'Mapping'
''' 

        with captured_output() as (out, err):
            node, c = self.checkChains(
                code, 
                    ['annotations -> ()',
                    'TypeAlias -> (TypeAlias -> (), TypeAlias -> (), TypeAlias -> ())',
                    'Mapping -> ()',
                    'Dict -> ()',
                    'Type -> (Type -> (Subscript -> ()))',
                    'C -> (C -> (Attribute -> ()), C -> (Attribute -> ()), C -> (Attribute -> '
                    '(Attribute -> ())))',
                    'Thing -> (Thing -> (), Thing -> (Subscript -> ()), TypeAlias -> ())'], 
                strict=False
            )
        produced_messages = out.getvalue().strip().split("\n")

        expected_warnings = [
            "W: unbound identifier 'field'",
            "W: unbound identifier 'D'",
        ]

        assert len(produced_messages) == len(expected_warnings), len(produced_messages)
        assert all(any(w in pw for pw in produced_messages) for w in expected_warnings)

        # locals of C
        self.assertEqual(c.dump_chains(node.body[-2]), 
                         ['method -> ()',
                            'method -> ()',
                            'method -> ()',
                            'method -> ()',
                            'field -> (field -> (), field -> (), TypeAlias -> ())',
                            'D -> (D -> ())'])
        
        # locals of D
        self.assertEqual(c.dump_chains(node.body[-2].body[-1]), 
                         ['field2 -> (TypeAlias -> (), field2 -> (), field2 -> ())',
                            'method -> ()',
                            'method -> ()',
                            'method -> ()',
                            'method -> ()',
                            'Thing -> ()'])

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_pep563_self_referential_annotation(self):
        code = '''
"""
module docstring
"""
from __future__ import annotations
class B:
    A: A # this should point to the top-level class
class A:
    A: 'str'
'''
        self.checkChains(
                code, 
                ['annotations -> ()',
                 'B -> ()', 
                 'A -> (A -> ())'], # good
                strict=False
            )

        code = '''
from __future__ import annotations
class A:
    A: 'str'
class B:
    A: A # this should point to the top-level class
'''
        self.checkChains(
                code, 
                ['annotations -> ()',
                 'A -> (A -> ())', 
                 'B -> ()'], 
                strict=False
            )
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_wilcard_import_annotation(self):
        code = '''
from typing import *
primes: List[int] # should resolve to the star
        '''

        self.checkChains(
                code, 
                ['* -> (List -> (Subscript -> ()))', 'primes -> (Subscript -> ())'],
                strict=False
            )
        # same with 'from __future__ import annotations'
        self.checkChains(
                'from __future__ import annotations\n' + code, 
                ['annotations -> ()', '* -> (List -> (Subscript -> ()))', 'primes -> (Subscript -> ())'],
                strict=False
            )
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_wilcard_import_annotation_and_global_scope(self):
        # we might argue that it should resolve to both the wildcard 
        # defined name and the type alias, but we're currently ignoring these
        # kind of scenarios.
        code = '''
from __future__ import annotations
from typing import *
primes: List[int]
List = list
    '''

        self.checkChains(
                code, 
                ['annotations -> ()',
                '* -> ()',
                'primes -> (Subscript -> ())',
                'List -> (List -> (Subscript -> ()))'],
                strict=False
            )
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_in_functions_locals(self):
        
        code = '''
class A:... # this one for pep 563 style
def generate():
    class A(int):... # this one for runtime style
    class C:
        field: A = 1
        def method(self, arg: A) -> None: ...
    return C
X = generate()
        '''

        # runtime style
        mod, chains = self.checkChains(
                code, 
                ['A -> ()', 
                 'generate -> (generate -> (Call -> ()))', 
                 'X -> ()'],
            )
        self.assertEqual(chains.dump_chains(mod.body[1]), 
                         ['A -> (A -> (), A -> ())', 
                          'C -> (C -> ())'])

        # pep 563 style
        mod, chains = self.checkChains(
                'from __future__ import annotations\n' + code, 
                ['annotations -> ()', 
                 'A -> (A -> (), A -> ())',
                 'generate -> (generate -> (Call -> ()))', 
                 'X -> ()'],
            )
        self.assertEqual(chains.dump_chains(mod.body[2]), 
                         ['A -> ()', 
                          'C -> (C -> ())'])

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_in_inner_functions_locals(self):

        code = '''
mytype = mytype2 = object
def outer():
    def middle():
        def inner(a:mytype, b:mytype2): pass
        class mytype(str):
            ...
        return inner
    class mytype2(int):
        ...
    return middle()
fn = outer()
        '''

        mod = ast.parse(code)
        chains = beniget.DefUseChains('test')
        with captured_output() as (out, err):
            chains.visit(mod)
        
        produced_messages = out.getvalue().strip().split("\n")

        self.assertEqual(produced_messages, ["W: unbound identifier 'mytype' at test:5:20"])

        self.assertEqual(
                chains.dump_chains(mod), 
                ['mytype -> ()', 
                 'mytype2 -> ()', 
                 'outer -> (outer -> (Call -> ()))', 
                 'fn -> ()'],
            )
        
        self.assertEqual(chains.dump_chains(mod.body[1]), 
                         ['middle -> (middle -> (Call -> ()))', 
                          'mytype2 -> (mytype2 -> ())'])
        self.assertEqual(chains.dump_chains(mod.body[1].body[0]), 
                         ['inner -> (inner -> ())', 
                          'mytype -> ()']) # annotation is unbound, so not linked here (and a warning is emitted)

        # in this case, the behaviour changes radically with pep 563

        mod, chains = self.checkChains(
                'from __future__ import annotations\n' + code, 
                ['annotations -> ()', 
                 'mytype -> (mytype -> ())', 
                 'mytype2 -> (mytype2 -> ())', 
                 'outer -> (outer -> (Call -> ()))', 
                 'fn -> ()'],
            )
        self.assertEqual(chains.dump_chains(mod.body[2]), 
                         ['middle -> (middle -> (Call -> ()))', 
                          'mytype2 -> ()'])
        self.assertEqual(chains.dump_chains(mod.body[2].body[0]), 
                         ['inner -> (inner -> ())', 
                          'mytype -> ()'])

        # but if we remove 'mytype = mytype2 = object' and 
        # keep the __future__ import then all anotations refers 
        # to the inner classes. 

    def test_lookup_scopes(self):
        #from beniget.beniget import _get_lookup_scopes
        from scalpel.duc import _get_lookup_scopes
        mod, fn, cls, lambd, gen, comp = ast.Module(), ast.FunctionDef(), ast.ClassDef(), ast.Lambda(), ast.GeneratorExp(), ast.DictComp()
        assert _get_lookup_scopes((mod, fn, fn, fn, cls)) == [mod, fn, fn, fn, cls]
        assert _get_lookup_scopes((mod, fn, fn, fn, cls, fn)) == [mod, fn, fn, fn, fn]
        assert _get_lookup_scopes((mod, cls, fn)) == [mod, fn]
        assert _get_lookup_scopes((mod, cls, fn, cls, fn)) == [mod, fn, fn]
        assert _get_lookup_scopes((mod, cls, fn, lambd, gen)) == [mod, fn, lambd, gen]
        assert _get_lookup_scopes((mod, fn, comp)) == [mod, fn, comp]
        assert _get_lookup_scopes((mod, fn)) == [mod, fn]
        assert _get_lookup_scopes((mod, cls)) == [mod, cls]
        assert _get_lookup_scopes((mod,)) == [mod]

        with self.assertRaises(ValueError, msg='invalid heads: must include at least one element'):
            _get_lookup_scopes(())

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_inner_inner_fn(self):
        code = '''
def outer():
    def middle():
        def inner(a:mytype): 
            ...
    class mytype(str):...
'''
        mod, chains = self.checkChains(
                code, 
                ['outer -> ()',],
            )
        self.assertEqual(chains.dump_chains(mod.body[0]), 
                         ['middle -> ()',
                          'mytype -> (mytype -> ())'])

        mod, chains = self.checkChains(
            'from __future__ import annotations\n' + code,
             ['annotations -> ()',
              'outer -> ()',],
        )
        self.assertEqual(chains.dump_chains(mod.body[1]), 
                         ['middle -> ()',
                          'mytype -> (mytype -> ())'])
    

    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_annotation_very_nested(self):
        
        # this code does not produce any pyright warnings
        code = '''
from __future__ import annotations

# when the following line is defined, 
# all annotations references points to it.
# when it's not defined, all anotation points
# to the inner classes. 
# in both cases pyright doesn't report any errors.
mytype = mytype2 = object

def outer():
    def middle():
        def inner(a:mytype, b:mytype2): 
            return getattr(a, 'count')(b)
        class mytype(str):
            class substr(int):
                ...
            def count(self, sep:substr) -> mytype:
                def c(x:mytype, y:mytype2) -> mytype:
                    return mytype('{},{}'.format(x,y))
                return c(self, mytype2(sep))
        return inner(mytype(), mytype2())
    class mytype2(int):
        ...
    return middle()
fn = outer()
        '''

        mod, chains = self.checkChains(
                code, 
                ['annotations -> ()',
                'mytype -> (mytype -> (), mytype -> (), mytype -> (), mytype -> ())',
                'mytype2 -> (mytype2 -> (), mytype2 -> ())',
                'outer -> (outer -> (Call -> ()))',
                'fn -> ()'],
            )
        self.assertEqual(chains.dump_chains(mod.body[2]), 
                         ['middle -> (middle -> (Call -> ()))',
                          'mytype2 -> (mytype2 -> (Call -> (Call -> ())), '
                          'mytype2 -> (Call -> (Call -> ())))'])
        self.assertEqual(chains.dump_chains(mod.body[2].body[0]), 
                         ['inner -> (inner -> (Call -> ()))',
                          'mytype -> (mytype -> (Call -> (Call -> ())), mytype -> (Call -> ()))'])

        mod, chains = self.checkChains(
                code.replace('mytype = mytype2 = object', 'pass'), 
                ['annotations -> ()',
                'outer -> (outer -> (Call -> ()))',
                'fn -> ()'],
            )
        self.assertEqual(chains.dump_chains(mod.body[2]), 
                         ['middle -> (middle -> (Call -> ()))',
                          'mytype2 -> (mytype2 -> (Call -> (Call -> ())), '
                                       'mytype2 -> (Call -> (Call -> ())), '
                                       'mytype2 -> (), '
                                       'mytype2 -> ())'])
        self.assertEqual(chains.dump_chains(mod.body[2].body[0]), 
                         ['inner -> (inner -> (Call -> ()))',
                          'mytype -> (mytype -> (Call -> (Call -> ())), '
                                     'mytype -> (Call -> ()), '
                                     'mytype -> (), '
                                     'mytype -> (), '
                                     'mytype -> (), '
                                     'mytype -> ())'])
    
    @skipIf(sys.version_info.major < 3, "Python 3 syntax")
    def test_pep563_type_alias_override_class(self):
        code = '''
from __future__ import annotations
class B:
    A: A # this should point to the top-level alias
class A:
    A: A # this should point to the top-level alias
A = bytes
'''
        self.checkChains(
                code, 
                ['annotations -> ()',
                 'B -> ()', 
                 'A -> ()',
                 'A -> (A -> (), A -> ())'], # good
                strict=False
            )
        
class TestUseDefChains(TestCase):
    def checkChains(self, code, ref):
        class StrictDefUseChains(beniget.DefUseChains):
            def unbound_identifier(self, name, node):
                raise RuntimeError(
                    "W: unbound identifier '{}' at {}:{}".format(
                        name, node.lineno, node.col_offset
                    )
                )

        node = ast.parse(code)
        c = StrictDefUseChains()
        c.visit(node)
        cc = beniget.UseDefChains(c)

        self.assertEqual(str(cc), ref)

    def test_simple_expression(self):
        code = "a = 1; a"
        self.checkChains(code, "a <- {a}, a <- {}")

    def test_call(self):
        code = "from foo import bar; bar(1, 2)"
        self.checkChains(code, "Call <- {Constant, Constant, bar}, bar <- {bar}")
