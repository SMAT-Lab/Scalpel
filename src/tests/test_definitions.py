from textwrap import dedent
from unittest import TestCase
import gast as ast
import scalpel._duc as beniget
import sys


class StrictDefUseChains(beniget.DefUseChains):
    def unbound_identifier(self, name, node):
        raise RuntimeError(
            "W: unbound identifier '{}' at {}:{}".format(
                name, node.lineno, node.col_offset
            )
        )


class TestGlobals(TestCase):
    def checkGlobals(self, code, ref):
        node = ast.parse(code)
        c = StrictDefUseChains()
        c.visit(node)
        self.assertEqual(c.dump_definitions(node), ref)

    def test_SingleFunctionDef(self):
        code = "def foo(): pass"
        self.checkGlobals(code, ["foo"])

    def test_MultipleFunctionDef(self):
        code = "def foo(): pass\ndef bar(): return"
        self.checkGlobals(code, ["bar", "foo"])

    def testFuntionRedefinion(self):
        code = "def foo(): pass\ndef foo(): return"
        self.checkGlobals(code, ["foo", "foo"])

    def testFuntionNested(self):
        code = "def foo():\n def bar(): return"
        self.checkGlobals(code, ["foo"])

    if sys.version_info.major >= 3:

        def testAsyncFunctionDef(self):
            code = "async def foo(): pass"
            self.checkGlobals(code, ["foo"])

    def testClassDef(self):
        code = "class C:pass"
        self.checkGlobals(code, ["C"])

    def testDelClassDef(self):
        code = "class C:pass\ndel C"
        self.checkGlobals(code, ["C"])

    def testDelClassDefReDef(self):
        code = "class C:pass\ndel C\nclass C:pass"
        self.checkGlobals(code, ["C", "C"])

    def testNestedClassDef(self):
        code = "class C:\n class D: pass"
        self.checkGlobals(code, ["C"])

    def testMultipleClassDef(self):
        code = "class C: pass\nclass D: pass"
        self.checkGlobals(code, ["C", "D"])

    def testClassRedefinition(self):
        code = "class C: pass\nclass C: pass"
        self.checkGlobals(code, ["C", "C"])

    def testClassMethodDef(self):
        code = "class C:\n def some(self):pass"
        self.checkGlobals(code, ["C"])

    def testGlobalDef(self):
        code = "x = 1"
        self.checkGlobals(code, ["x"])

    if sys.version_info.major >= 3:

        def testGlobalAnnotatedDef(self):
            code = "x : 1"
            self.checkGlobals(code, ["x"])

    def testMultipleGlobalDef(self):
        code = "x = 1; x = 2"
        self.checkGlobals(code, ["x", "x"])

    def testGlobalDestructuring(self):
        code = "x, y = 1, 2"
        self.checkGlobals(code, ["x", "y"])

    if sys.version_info.major >= 3:
        def testGlobalStarredDestructuring(self):
            code = "x, *y = 1, [2]"
            self.checkGlobals(code, ["x", "y"])

    def testGlobalAugAssign(self):
        code = "x = 1; x += 2"
        self.checkGlobals(code, ["x"])

    def testGlobalFor(self):
        code = "for x in (1,2): pass"
        self.checkGlobals(code, ["x"])

    def testGlobalForDestructuring(self):
        code = "for x, y in [(1,2)]: pass"
        self.checkGlobals(code, ["x", "y"])

    def testGlobalNestedFor(self):
        code = "for x in (1,2):\n for y in (2, 1): pass"
        self.checkGlobals(code, ["x", "y"])

    def testGlobalInFor(self):
        code = "for x in (1,2): y = x"
        self.checkGlobals(code, ["x", "y"])

    if sys.version_info >= (3, 7):

        def testGlobalAsyncFor(self):
            code = "async for x in (1,2): pass"
            self.checkGlobals(code, ["x"])

    def testGlobalInWhile(self):
        code = "while True: x = 1"
        self.checkGlobals(code, ["x"])

    def testGlobalInIfTrueBranch(self):
        code = "if 1: a = 1"
        self.checkGlobals(code, ["a"])

    def testGlobalInIfFalseBranch(self):
        code = "if 1: pass\nelse: a = 1"
        self.checkGlobals(code, ["a"])

    def testGlobalInIfBothBranch(self):
        code = "if 1: a = 1\nelse: a = 2"
        self.checkGlobals(code, ["a", "a"])

    def testGlobalInIfBothBranchDifferent(self):
        code = "if 1: a = 1\nelse: b = 2"
        self.checkGlobals(code, ["a", "b"])

    def testGlobalWith(self):
        code = "from some import foo\nwith foo() as x: pass"
        self.checkGlobals(code, ["foo", "x"])

    if sys.version_info >= (3, 7):

        def testGlobalAsyncWith(self):
            code = "from some import foo\nasync with foo() as x: pass"
            self.checkGlobals(code, ["foo", "x"])

    def testGlobalTry(self):
        code = "try: x = 1\nexcept Exception: pass"
        self.checkGlobals(code, ["x"])

    def testGlobalTryExcept(self):
        code = "from some import foo\ntry: foo()\nexcept Exception as e: pass"
        self.checkGlobals(code, ["e", "foo"])

    def testGlobalTryExceptFinally(self):
        code = "try: w = 1\nexcept Exception as x: y = 1\nfinally: z = 1"
        self.checkGlobals(code, ["w", "x", "y", "z"])

    def testGlobalThroughKeyword(self):
        code = "def foo(): global x"
        # a global keyword does not actually create a global
        self.checkGlobals(code, ["foo"])

    def testGlobalThroughKeywordAndAssign(self):
        code = "def foo(): global x; x = 1"
        self.checkGlobals(code, ["foo", "x"])

    def testGlobalThroughMultipleKeyword(self):
        code = "def foo(): global x\ndef bar(): global x; x = 1"
        self.checkGlobals(code, ["bar", "foo", "x"])

    def testGlobalBeforeKeyword(self):
        code = "x = 1\ndef foo(): global x"
        self.checkGlobals(code, ["foo", "x"])

    def testGlobalsBeforeKeyword(self):
        code = "x = 1\ndef foo(): global x, y"
        self.checkGlobals(code, ["foo", "x"])

    if sys.version_info.major >= 3:

        def testGlobalAfterKeyword(self):
            code = "def foo(): global x\nx : 1"
            self.checkGlobals(code, ["foo", "x"])

        def testGlobalsAfterKeyword(self):
            code = "def foo(): global x, y\ny : 1"
            self.checkGlobals(code, ["foo", "y"])

    def testGlobalKeyworaInClassd(self):
        code = "class F: global x; x = 1"
        self.checkGlobals(code, ["F", "x"])

    def testGlobalImport(self):
        code = "import foo"
        self.checkGlobals(code, ["foo"])

    def testGlobalImports(self):
        code = "import foo, bar"
        self.checkGlobals(code, ["bar", "foo"])

    def testGlobalImportSubModule(self):
        code = "import foo.bar"
        self.checkGlobals(code, ["foo"])

    def testGlobalImportSubModuleAs(self):
        code = "import foo.bar as foobar"
        self.checkGlobals(code, ["foobar"])

    def testGlobalImportAs(self):
        code = "import foo as bar"
        self.checkGlobals(code, ["bar"])

    def testGlobalImportsAs(self):
        code = "import foo as bar, foobar"
        self.checkGlobals(code, ["bar", "foobar"])

    def testGlobalImportFrom(self):
        code = "from foo import bar"
        self.checkGlobals(code, ["bar"])

    def testGlobalImportFromAs(self):
        code = "from foo import bar as BAR"
        self.checkGlobals(code, ["BAR"])

    def testGlobalImportFromStar(self):
        code = "from foo import *"
        self.checkGlobals(code, ["*"])

    def testGlobalImportFromStarRedefine(self):
        code = "from foo import *\nx+=1"
        self.checkGlobals(code, ["*", "x"])

    def testGlobalImportsFrom(self):
        code = "from foo import bar, man"
        self.checkGlobals(code, ["bar", "man"])

    def testGlobalImportsFromAs(self):
        code = "from foo import bar, man as maid"
        self.checkGlobals(code, ["bar", "maid"])

    def testGlobalListComp(self):
        code = "from some import y; [1 for x in y]"
        if sys.version_info.major == 2:
            self.checkGlobals(code, ["x", "y"])
        else:
            self.checkGlobals(code, ["y"])

    def testGlobalSetComp(self):
        code = "from some import y; {1 for x in y}"
        if sys.version_info.major == 2:
            self.checkGlobals(code, ["x", "y"])
        else:
            self.checkGlobals(code, ["y"])

    def testGlobalDictComp(self):
        code = "from some import y; {1:1 for x in y}"
        if sys.version_info.major == 2:
            self.checkGlobals(code, ["x", "y"])
        else:
            self.checkGlobals(code, ["y"])

    def testGlobalGeneratorExpr(self):
        code = "from some import y; (1 for x in y)"
        if sys.version_info.major == 2:
            self.checkGlobals(code, ["x", "y"])
        else:
            self.checkGlobals(code, ["y"])

    def testGlobalLambda(self):
        code = "lambda x: x"
        self.checkGlobals(code, [])


class TestClasses(TestCase):
    def checkClasses(self, code, ref):
        node = ast.parse(code)
        c = StrictDefUseChains()
        c.visit(node)
        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        assert len(classes) == 1, "only one top-level function per test case"
        cls = classes[0]
        self.assertEqual(c.dump_definitions(cls), ref)

    def test_class_method_assign(self):
        code = "class C:\n def foo(self):pass\n bar = foo"
        self.checkClasses(code, ["bar", "foo"])


class TestLocals(TestCase):
    def checkLocals(self, code, ref):
        node = ast.parse(dedent(code))
        c = StrictDefUseChains()
        c.visit(node)
        functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        assert len(functions) == 1, "only one top-level function per test case"
        f = functions[0]
        self.assertEqual(c.dump_definitions(f), ref)

    def testLocalFunctionDef(self):
        code = "def foo(): pass"
        self.checkLocals(code, [])

    def testLocalFunctionDefOneArg(self):
        code = "def foo(a): pass"
        self.checkLocals(code, ["a"])

    def testLocalFunctionDefOneArgDefault(self):
        code = "def foo(a=1): pass"
        self.checkLocals(code, ["a"])

    def testLocalFunctionDefArgsDefault(self):
        code = "def foo(a, b=1): pass"
        self.checkLocals(code, ["a", "b"])

    def testLocalFunctionDefStarArgs(self):
        code = "def foo(a, *b): pass"
        self.checkLocals(code, ["a", "b"])

    def testLocalFunctionDefKwArgs(self):
        code = "def foo(a, **b): pass"
        self.checkLocals(code, ["a", "b"])

    if sys.version_info.major >= 3:

        def testLocalFunctionDefKwOnly(self):
            code = "def foo(a, *, b=1): pass"
            self.checkLocals(code, ["a", "b"])

    if sys.version_info.major == 2:

        def testLocalFunctionDefDestructureArg(self):
            code = "def foo((a, b)): pass"
            self.checkLocals(code, ["a", "b"])

    def test_LocalAssign(self):
        code = "def foo(): a = 1"
        self.checkLocals(code, ["a"])

    def test_LocalAssignRedef(self):
        code = "def foo(a): a = 1"
        self.checkLocals(code, ["a", "a"])
    
    def test_LocalAssignRedefIfElseOverride(self):
        code = """
            def foo(): 
                if NotImplemented:
                    x = 2
                else:
                    x = 3
                x = 0
        """
        self.checkLocals(code, ["x", "x", "x"])

    def test_LocalNestedFun(self):
        code = "def foo(a):\n def bar(): return a\n return bar"
        self.checkLocals(code, ["a", "bar"])

    if sys.version_info.major >= 3:

        def test_LocalNonLocalBefore(self):
            code = "def foo(a):\n def bar():\n  nonlocal a; a = 1\n bar(); return a"
            self.checkLocals(code, ["a", "bar"])

        def test_LocalNonLocalAfter(self):
            code = (
                "def foo():\n def bar():\n  nonlocal a; a = 1\n a = 2; bar(); return a"
            )
            self.checkLocals(code, ["a", "bar"])

        def test_LocalDestructuring(self):
            code = "def foo(x): y, *z = x"
            self.checkLocals(code, ["x", "y", "z"])

    def test_LocalMadeGlobal(self):
        code = "def foo(): global a; a = 1"
        self.checkLocals(code, [])

    def test_ListCompInLoop(self):
        code = "def foo(i):\n for j in i:\n  [k for k in j]"
        if sys.version_info.major == 2:
            self.checkLocals(code, ["i", "j", "k"])
        else:
            self.checkLocals(code, ["i", "j"])

    def test_AugAssignInLoop(self):
        code = """
def foo(X, f):
    for i in range(2):
        if i == 0: A = f * X[:, i]
        else: A += f * X[:, i]
    return A"""
        self.checkLocals(code, ["A", "X", "f", "i"])

    def test_IfInWhile(self):
        code = """
def foo(a):
    while(a):
        if a == 1: print(b)
        else: b = a"""
        self.checkLocals(code, ["a", "b"])

class TestDefIsLive(TestCase):

    def checkLocals(self, c, node, ref, only_live=False):
        self.assertEqual(sorted(c._dump_locals(node, only_live=only_live)), 
                         sorted(ref))
    
    def checkLiveLocals(self, code, livelocals, locals):
        node = ast.parse(dedent(code))
        c = StrictDefUseChains()
        c.visit(node)
        self.checkLocals(c, node, locals)
        self.checkLocals(c, node, livelocals, only_live=True)
        return node, c
    
    def test_LocalAssignRedefIfElseOverride(self):
        code = """
            if NotImplemented:
                x = 2
            else:
                x = 3
            x = 0
        """
        self.checkLiveLocals(code, ["x:6"], ["x:3,5,6"])
    
    def test_LocalAssignmentRedefInEachBranch(self):
        code = """
        x = 10
        if NotImplemented:
            x = 100
        else:
            x = 1000
        """
        self.checkLiveLocals(code, ["x:4,6"], ["x:2,4,6"])

    def test_AssignmentInsideBothBranchesOfTryExcept(self):
        code = """
            try:
                1 / 0
            except ZeroDivisionError:
                x = 10
            except RuntimeError:
                x = -1
        """
        self.checkLiveLocals(code, ["x:5,7"], ["x:5,7"])

    def test_AssignmentOverrideFinallyBlock(self):
        code = """
            try:
                1 / 0
            except ZeroDivisionError:
                x = 10
            except RuntimeError:
                x = -1
            finally:
                x = None
        """
        self.checkLiveLocals(code, ["x:9"], ["x:5,7,9"])
    
    def test_AssignmentSimple(self):
        code = """
            a = 1
            a = a + 1
            a = a + 1
            """
        self.checkLiveLocals(code, ["a:4"], ["a:2,3,4"])

    def test_BothLive(self):
        code = '''
        import sys
        if sys.version_info >= (3, 7, 0):
            _PY37PLUS = True
        else:
            _PY37PLUS = False
        '''
        if sys.version_info>=(3,10):
            self.checkLiveLocals(code, ["sys:2", "_PY37PLUS:4,6"], ["sys:2", "_PY37PLUS:4,6"])
        else:
            self.checkLiveLocals(code, ["sys:None", "_PY37PLUS:4,6"], ["sys:None", "_PY37PLUS:4,6"])
    
    def test_BuiltinNameRedefConditional(self):
        code = '''
        import sys
        class property:
            pass
        if sys.version_info >= (3, 11):
            class ExceptionGroup(Exception):
                @property
                def exceptions(self):
                    pass
        '''
        if sys.version_info>=(3,10):
            self.checkLiveLocals(code, ['sys:2', 'property:3', 'ExceptionGroup:6'], 
                                ['sys:2', 'property:3', 'ExceptionGroup:6'])
        else:
            self.checkLiveLocals(code, ['sys:None', 'property:3', 'ExceptionGroup:6'], 
                                ['sys:None', 'property:3', 'ExceptionGroup:6'])
    
    def test_loop_body_might_not_run(self):
        code = """
        i = 2
        while int: 
            i = 3
        """
        self.checkLiveLocals(code, ['i:2,4'], ['i:2,4'])
    
    def test_var_in_comp_doesnt_kill_upper_scope_var(self):
        code = '''
        x = True
        [x for x in (1,2)]
        '''
        if sys.version_info > (3,):
            node, c = self.checkLiveLocals(code, ['x:2'], ['x:2'])
            self.checkLocals(c, node.body[-1].value, ['x:3'], only_live=True)
        else:
            self.checkLiveLocals(code, ['x:3'], ['x:2,3'])


    def test_var_redef_in_method_scope(self):
        code = '''\
        v = True # not killed
        class C:
            v = True # killed
            v = False
            def __init__(self):
                v = 1 # killed
                v = False # not killed
        '''
        node, c = self.checkLiveLocals(code, ['v:1', 'C:2'], ['v:1', 'C:2'])
        self.checkLocals(c, node.body[-1], ['v:4', '__init__:5'], only_live=True)
        self.checkLocals(c, node.body[-1].body[-1], ['self:5', 'v:7'], only_live=True)
    
    def test_if_body_might_not_run(self):
        code = """
        i = 2
        if int: 
            i = 3
        """
        self.checkLiveLocals(code, ['i:2,4'], ['i:2,4'])

    def test_more_loops(self):
        # All variables here are live for beniget. Constant
        # folding with control-flow understanding will reveal 
        # that the else branch of the while loop is unreachable 
        # (so the k assignment is never executed).
        # But beniget over-approximate this.
        code = '''
        b = 1
        while True:
            v = 1
            if v:
                b = 2
                break
        else:
            v = [(1,3)]
            for v,k in v:
                pass
            else:
                k = 2
        '''
        self.checkLiveLocals(code, ['b:2,6', 'v:9,10,4', 'k:10,13'],  
                                ['b:2,6', 'v:9,10,4', 'k:10,13'])

