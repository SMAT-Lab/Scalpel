import ast
import textwrap
from typing import (List, Optional, Tuple)
from scalpel.cfg import CFGBuilder
from scalpel.duc import Definition, DUC, Reference

def make_ast(src:str):
    return ast.parse(textwrap.dedent(src))

def make_duc(name: str, src: str) -> DUC:
    ast_node = make_ast(src)
    cfg_dict = CFGBuilder().build(name, ast_node, flattened=True)
    return DUC(cfg_dict)


def assert_num_defs_refs(duc: DUC, num_defs: int, num_refs: int, *args) -> None:
    defs, refs = map(list, duc.get_all_definitions_and_references(*args))
    assert len(defs) == num_defs, f"expected {num_defs} definitions, got {len(defs)}"
    assert len(refs) == num_refs, f"expected {num_refs} references, got {len(refs)}"

def get_defs(duc: DUC, num: int, *args) -> List[Definition]:
    defs = list(duc.get_definitions(*args))
    assert len(defs) == num, f"expected {num} definitions, got {len(defs)}"
    return defs

def get_def(duc: DUC, *args) -> Definition:
    return get_defs(duc, 1, *args)[0]

def get_refs(duc: DUC, num: int, *args) -> List[Reference]:
    refs = list(duc.get_references(*args))
    assert len(refs) == num, f"expected {num} references, got {len(refs)}"
    return refs

def get_ref(duc: DUC, *args) -> Reference:
    return get_refs(duc, 1, *args)[0]

def test_definitions_and_references() -> None:
    def test_simple() -> None:
        duc = make_duc(
            "simple",
            """\
            a = 1
            print(a + 1) 
            """,
        )
        a_def = get_def(duc, "a")
        a_ref = get_ref(duc, "a")
        print_ref = get_ref(duc, "print")

        #assert_num_defs_refs(duc, 1, 2)
        #assert len(print_ref.name.counters) == 0
        #assert isinstance(a_def.ast_node, ast.Constant)
        #assert len(a_ref.name.counters) == 1
        
    def test_reassign() -> None:
        duc = make_duc(
            "reassign",
            """\
            a = 1
            print(a)
            a = 2
            print(a)
            """,
        )

        assert_num_defs_refs(duc, 2, 4)

        a_def1, a_def2 = get_defs(duc, 2, "a")
        assert a_def1.ast_node.lineno == 1
        assert a_def2.ast_node.lineno == 3

        a_ref1, a_ref2 = get_refs(duc, 2, "a")
        assert a_ref1.stmt_idx == 1
        assert a_ref2.stmt_idx == 3

    def test_ssa_example() -> None:
        duc = make_duc(
            "ssa_example",
            """\
            b = 10
            if b > 0:
                a = a + b
            else:
                a = 10
            print(a)
            """,
        )

        assert_num_defs_refs(duc, 3, 5)

        a_def1, a_def2 = get_defs(duc, 2, "a")
        assert a_def1.ast_node.lineno == 3
        assert a_def2.ast_node.lineno == 5

        get_refs(duc, 2, "b")

        a_ref1, a_ref2 = get_refs(duc, 2, "a")
        assert len(a_ref1.name.counters) == 0
        assert len(a_ref2.name.counters) == 2

    def test_multiple_scopes() -> None:
        duc = make_duc(
            "multiple_scopes",
            """\
            a = 1
            def f():
                a = 2
                b = 3
            """,
        )
        #_, f_scope = duc.get_lexical_scopes()

        #assert_num_defs_refs(duc, 2, 0)
        #a_def = get_def(duc, "a")
        #assert isinstance(a_def.ast_node, ast.Constant)
        #assert a_def.ast_node.lineno == 1
        #f_def = get_def(duc, "f")
        #assert isinstance(f_def.ast_node, ast.FunctionDef)

        #assert_num_defs_refs(duc, 2, 0, f_scope)
        #f_a_def = get_def(duc, "a", f_scope)
        #assert isinstance(f_a_def.ast_node, ast.Constant)
        #assert f_a_def.ast_node.lineno == 3
        #f_b_def = get_def(duc, "b", f_scope)
        #assert isinstance(f_b_def.ast_node, ast.Constant)

    def test_classes() -> None:
        duc = make_duc(
            "classes",
            """\
            a = 1
            class C:
                a = 2
                b = a
                def f(self):
                    x = a + b
            print(a)
            """,
        )
        _, c_scope, c_f_scope = duc.get_lexical_scopes()

        assert_num_defs_refs(duc, 2, 2)
        assert get_def(duc, "a").ast_node.lineno == 1
        global_a_ref = get_ref(duc, "a")
        assert duc.ast_node_for_reference(global_a_ref).lineno == 7  # print(a)

        assert_num_defs_refs(duc, 3, 1, c_scope)
        a_def = get_def(duc, "a", c_scope)
        assert a_def.ast_node.lineno == 3
        a_ref = get_ref(duc, "a", c_scope)
        assert duc.ast_node_for_reference(a_ref, c_scope).lineno == 4  # b = a

        assert_num_defs_refs(duc, 1, 2, c_f_scope)
        x_def = get_def(duc, "x", c_f_scope)
        assert isinstance(x_def.ast_node, ast.BinOp)

    def test_multiple_defs() -> None:
        duc = make_duc(
            "multiple_defs",
            """\
            a = 1
            for a in range(5):
                pass
            def f(a, b):
                print(a, b)
            """,
        )
        _, f_scope = duc.get_lexical_scopes()

        assert_num_defs_refs(duc, 3, 1)
        global_a_def1, global_a_def2 = get_defs(duc, 2, "a")
        assert isinstance(global_a_def1.ast_node, ast.Constant)
        assert isinstance(global_a_def2.ast_node, ast.Call)
        f_def = get_def(duc, "f")
        assert isinstance(f_def.ast_node, ast.FunctionDef)
        get_refs(duc, 0, "a")

        assert_num_defs_refs(duc, 0, 3, f_scope)
        # a_def = get_def(f_duc, "a")
        # assert isinstance(a_def.ast_node, ast.arg)
        # b_def = get_def(f_duc, "b")
        # assert isinstance(b_def, ast.arg)

    test_simple()
    #test_reassign()
    #test_ssa_example()
    #test_multiple_scopes()
    #test_classes()
    #test_multiple_defs()


def test_relationships(src: str, *expected: Tuple[str, Optional[str], str]) -> None:
    relationships = list(make_duc(src, src).container_relationships())
    assert len(relationships) == len(expected), (
        f"{src}: expected"
        f" {len(expected)} relationship{'' if len(expected) == 1 else 's'}, got"
        f" {len(relationships)}"
    )
    for (container, (key, value)), (
        expected_container,
        expected_key,
        expected_value,
    ) in zip(relationships, expected):
        assert (
            container.name == expected_container
        ), f"{src}: expected container {expected_container}, got {container.name}"
        assert (
            key is None if expected_key is None else key and key.name == expected_key
        ), f"{src}: expected key {expected_key}, got {key}"
        assert (
            value.name == expected_value
        ), f"{src}: expected value {expected_value}, got {value}"


def test_container_relationships() -> None:
    def test_simple():
        for method in ("add", "append", "appendleft"):
            test_relationships(f"a.{method}(b)", ("a", None, "b"))

        test_relationships("a.insert(b, c)", ("a", None, "c"))

        test_relationships("a += [b, c, 1]", ("a", None, "b"), ("a", None, "c"))
        test_relationships("a |= {b, c, 1}", ("a", None, "b"), ("a", None, "c"))

        test_relationships(
            "a.update({b: c, d: e, 'f': g})",
            ("a", "b", "c"),
            ("a", "d", "e"),
            ("a", None, "g"),
        )
        test_relationships(
            "a.update(b=c, d=e, f=1)",
            ("a", None, "c"),
            ("a", None, "e"),
        )
        test_relationships(
            "a.update({b: c, d: e}, f=g)",
            ("a", "b", "c"),
            ("a", "d", "e"),
            ("a", None, "g"),
        )
        test_relationships(
            "a |= {b: c, d: e, 'f': g}",
            ("a", "b", "c"),
            ("a", "d", "e"),
            ("a", None, "g"),
        )

        test_relationships("a = b + [c, d]", ("a", None, "c"), ("a", None, "d"))
        test_relationships(
            "a = {b} | {c, d}",
            ("a", None, "b"),
            ("a", None, "c"),
            ("a", None, "d"),
        )
        test_relationships(
            "a = {b: c} | d",
            ("a", "b", "c"),
        )
        test_relationships(
            "a = b = c.d = [e, f] + [g]",
            ("a", None, "e"),
            ("a", None, "f"),
            ("a", None, "g"),
            ("b", None, "e"),
            ("b", None, "f"),
            ("b", None, "g"),
        )
        test_relationships(
            "a: T = {b} | c",
            ("a", None, "b"),
        )

    def test_no_relationships() -> None:
        for src in (
            "a.foo(b)",
            "a + b",
            "a += b",
            "a + {b}",
            "a - [b]",
            "a | [b]",
            "a = b + c",
            "a = b | c",
            "a = {b} + c",
            "a = [b] | c",
            "a: T",
            "a.insert(b)",
            "a.insert(*b, c)",
            "a.update()",
            "a.update(b)",
        ):
            num_relationships = len(list(make_duc(src, src).container_relationships()))
            assert num_relationships == 0, (
                f"expected {src} to have no container relationships, got"
                f" {num_relationships} relationships"
            )

    def test_counters() -> None:
        duc = make_duc(
            "counters",
            """\
            d = {}
            if foo():
                v = 0
            else:
                v = 1
            d[k] = v
            """,
        )
        ((container, (key, value)),) = duc.container_relationships()
        assert container.counters == {0}
        assert key and key.counters == set()
        assert value.counters == {0, 1}

    #test_simple()
    #test_no_relationships()
    #test_counters()


def main() -> None:
    test_definitions_and_references()
    #test_container_relationships()


if __name__ == "__main__":
    main()
