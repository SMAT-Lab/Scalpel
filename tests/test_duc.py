import ast
import textwrap
from typing import Iterator, List
from scalpel.duc import Definition, DUC, Reference, Scope, ducs_from_src


def make_ducs(name: str, src: str) -> Iterator[DUC]:
    return ducs_from_src(name, textwrap.dedent(src))


def assert_num_defs_refs(
    duc: DUC, num_defs: int, num_refs: int, scope: Scope = None
) -> None:
    defs, refs = duc.get_definitions_and_references(scope)
    assert len(defs) == num_defs, f"expected {num_defs} definitions, got {len(defs)}"
    assert len(refs) == num_refs, f"expected {num_refs} references, got {len(refs)}"


def get_defs(duc: DUC, num: int, name: str, scope: Scope = None) -> List[Definition]:
    defs = duc.get_definitions(name, scope)
    assert len(defs) == num, f"expected {num} definitions, got {len(defs)}"
    return defs


def get_def(duc: DUC, name: str, scope: Scope = None) -> Definition:
    return get_defs(duc, 1, name, scope)[0]


def get_refs(duc: DUC, num: int, name: str, scope: Scope = None) -> List[Reference]:
    refs = duc.get_references(name, scope)
    assert len(refs) == num, f"expected {num} references, got {len(refs)}"
    return refs


def get_ref(duc: DUC, name: str, scope: Scope = None) -> Reference:
    return get_refs(duc, 1, name, scope)[0]


def test_simple() -> None:
    (duc,) = make_ducs(
        "simple",
        """\
        a = 1
        print(a + 1)
        """,
    )
    assert len(list(duc.get_lexical_scopes())) == 1

    assert_num_defs_refs(duc, 1, 2)
    a_def = get_def(duc, "a")
    assert isinstance(a_def.ast_node, ast.Constant)
    a_ref = get_ref(duc, "a")
    assert len(a_ref.name_counters) == 1
    print_ref = get_ref(duc, "print")
    assert len(print_ref.name_counters) == 0


def test_reassign() -> None:
    (duc,) = make_ducs(
        "reassign",
        """\
        a = 1
        print(a)
        a = 2
        print(a)
        """,
    )
    assert len(list(duc.get_lexical_scopes())) == 1

    assert_num_defs_refs(duc, 2, 4)

    a_def1, a_def2 = get_defs(duc, 2, "a")
    assert a_def1.ast_node.lineno == 1
    assert a_def2.ast_node.lineno == 3

    a_ref1, a_ref2 = get_refs(duc, 2, "a")
    assert a_ref1.stmt_idx == 1
    assert a_ref2.stmt_idx == 3


def test_ssa_example() -> None:
    (duc,) = make_ducs(
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
    assert len(list(duc.get_lexical_scopes())) == 1

    assert_num_defs_refs(duc, 3, 5)

    a_def1, a_def2 = get_defs(duc, 2, "a")
    assert a_def1.ast_node.lineno == 3
    assert a_def2.ast_node.lineno == 5

    get_refs(duc, 2, "b")

    a_ref1, a_ref2 = get_refs(duc, 2, "a")
    assert len(a_ref1.name_counters) == 0
    assert len(a_ref2.name_counters) == 2


def test_multiple_scopes() -> None:
    global_duc, f_duc = make_ducs(
        "multiple_scopes",
        """\
        a = 1
        def f():
            a = 2
            b = 3
        """,
    )

    scopes = list(global_duc.get_lexical_scopes())
    assert len(scopes) == 2
    global_scope, f_scope = scopes

    assert_num_defs_refs(global_duc, 2, 0)
    a_def = get_def(global_duc, "a")
    assert isinstance(a_def.ast_node, ast.Constant)
    assert a_def.ast_node.lineno == 1
    f_def = get_def(global_duc, "f")
    assert isinstance(f_def.ast_node, ast.FunctionDef)

    assert_num_defs_refs(f_duc, 2, 0)
    f_a_def = get_def(f_duc, "a")
    assert isinstance(f_a_def.ast_node, ast.Constant)
    assert f_a_def.ast_node.lineno == 3
    assert f_a_def == get_def(global_duc, "a", scope=f_scope)
    f_b_def = get_def(f_duc, "b")
    assert isinstance(f_b_def.ast_node, ast.Constant)
    assert f_b_def == get_def(global_duc, "b", scope=f_scope)


def test_classes() -> None:
    global_duc, c_duc, c_f_duc = make_ducs(
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

    scopes = list(global_duc.get_lexical_scopes())
    assert len(scopes) == 3
    global_scope, c_scope, c_f_scope = scopes

    assert_num_defs_refs(global_duc, 2, 2)
    assert get_def(global_duc, "a").ast_node.lineno == 1
    global_a_ref = get_ref(global_duc, "a")
    assert global_duc.ast_node_for_reference(global_a_ref).lineno == 7  # print(a)

    assert_num_defs_refs(c_duc, 3, 1)
    a_def = get_def(c_duc, "a")
    assert a_def.ast_node.lineno == 3
    assert a_def == get_def(global_duc, "a", scope=c_scope)
    a_ref = get_ref(c_duc, "a")
    assert c_duc.ast_node_for_reference(a_ref).lineno == 4  # b = a
    assert a_ref == get_ref(global_duc, "a", scope=c_scope)

    assert_num_defs_refs(c_f_duc, 1, 2)
    x_def = get_def(c_f_duc, "x")
    assert isinstance(x_def.ast_node, ast.BinOp)
    assert x_def == get_def(c_duc, "x", scope=c_f_scope)


def test_multiple_defs() -> None:
    global_duc, f_duc = make_ducs(
        "multiple_defs",
        """\
        a = 1
        for a in range(5):
            pass
        def f(a, b):
            print(a, b)
        """,
    )

    scopes = list(global_duc.get_lexical_scopes())
    assert len(scopes) == 2
    global_scope, f_scope = scopes

    assert_num_defs_refs(global_duc, 3, 1)
    global_a_def1, global_a_def2 = get_defs(global_duc, 2, "a")
    assert isinstance(global_a_def1.ast_node, ast.Constant)
    assert isinstance(global_a_def2.ast_node, ast.Call)
    f_def = get_def(global_duc, "f")
    assert isinstance(f_def.ast_node, ast.FunctionDef)
    get_refs(global_duc, 0, "a")

    assert_num_defs_refs(f_duc, 0, 3)
    # a_def = get_def(f_duc, "a")
    # assert isinstance(a_def.ast_node, ast.arg)
    # assert a_def == get_def(global_duc, "a", scope=f_scope)
    # b_def = get_def(f_duc, "b")
    # assert isinstance(b_def, ast.arg)
    # assert b_def == get_def(global_duc, "b", scope=f_scope)


def main() -> None:
    test_simple()
    test_reassign()
    test_ssa_example()
    test_multiple_scopes()
    test_classes()
    test_multiple_defs()


if __name__ == "__main__":
    main()
