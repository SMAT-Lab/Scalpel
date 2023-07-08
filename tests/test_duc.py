import ast
import textwrap
from typing import List
from scalpel.cfg import CFGBuilder
from scalpel.duc import Definition, DUC, Reference


def make_duc(name: str, src: str) -> DUC:
    return DUC(CFGBuilder().build_from_src(name, textwrap.dedent(src)))


def assert_num_defs_refs(duc: DUC, num_defs: int, num_refs: int, *args) -> None:
    defs, refs = duc.get_definitions_and_references(*args)
    assert len(defs) == num_defs, f"expected {num_defs} definitions, got {len(defs)}"
    assert len(refs) == num_refs, f"expected {num_refs} references, got {len(refs)}"


def get_defs(duc: DUC, num: int, *args) -> List[Definition]:
    defs = duc.get_definitions(*args)
    assert len(defs) == num, f"expected {num} definitions, got {len(defs)}"
    return defs


def get_def(duc: DUC, *args) -> Definition:
    return get_defs(duc, 1, *args)[0]


def get_refs(duc: DUC, num: int, *args) -> List[Reference]:
    refs = duc.get_references(*args)
    assert len(refs) == num, f"expected {num} references, got {len(refs)}"
    return refs


def get_ref(duc: DUC, *args) -> Reference:
    return get_refs(duc, 1, *args)[0]


def test_simple() -> None:
    duc = make_duc(
        "simple",
        """\
        a = 1
        print(a + 1)
        """,
    )

    assert_num_defs_refs(duc, 1, 2)
    a_def = get_def(duc, "a")
    assert isinstance(a_def.ast_node, ast.Constant)
    a_ref = get_ref(duc, "a")
    assert len(a_ref.name_counters) == 1
    print_ref = get_ref(duc, "print")
    assert len(print_ref.name_counters) == 0


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
    assert len(a_ref1.name_counters) == 0
    assert len(a_ref2.name_counters) == 2


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
    _, f_scope = duc.get_lexical_scopes()

    assert_num_defs_refs(duc, 2, 0)
    a_def = get_def(duc, "a")
    assert isinstance(a_def.ast_node, ast.Constant)
    assert a_def.ast_node.lineno == 1
    f_def = get_def(duc, "f")
    assert isinstance(f_def.ast_node, ast.FunctionDef)

    assert_num_defs_refs(duc, 2, 0, f_scope)
    f_a_def = get_def(duc, "a", f_scope)
    assert isinstance(f_a_def.ast_node, ast.Constant)
    assert f_a_def.ast_node.lineno == 3
    f_b_def = get_def(duc, "b", f_scope)
    assert isinstance(f_b_def.ast_node, ast.Constant)


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


def main() -> None:
    test_simple()
    test_reassign()
    test_ssa_example()
    test_multiple_scopes()
    test_classes()
    test_multiple_defs()


if __name__ == "__main__":
    main()
