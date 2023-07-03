import ast
import textwrap
from typing import List
from scalpel.cfg import CFGBuilder
from scalpel.duc import Definition, DUC, Reference


def make_duc(name: str, src: str) -> DUC:
    return DUC(
        CFGBuilder().build_from_src(
            name,
            textwrap.dedent(src),
        )
    )


def assert_num_defs_refs(duc: DUC, scope: str, num_defs: int, num_refs: int) -> None:
    defs, refs = duc.get_definitions_and_references(scope)
    assert len(defs) == num_defs, f"expected {num_defs} definitions, got {len(defs)}"
    assert len(refs) == num_refs, f"expected {num_refs} references, got {len(refs)}"


def get_defs(duc: DUC, scope: str, name: str, num: int) -> List[Definition]:
    defs = duc.get_definitions(scope, name)
    assert len(defs) == num, f"expected {num} definitions, got {len(defs)}"
    return defs


def get_def(duc: DUC, scope: str, name: str) -> Definition:
    return get_defs(duc, scope, name, 1)[0]


def get_refs(duc: DUC, scope: str, name: str, num: int) -> List[Reference]:
    refs = duc.get_refs(scope, name)
    assert len(refs) == num, f"expected {num} references, got {len(refs)}"
    return refs


def get_ref(duc: DUC, scope: str, name: str) -> Reference:
    return get_refs(duc, scope, name, 1)[0]


def get_global_scope(duc: DUC) -> str:
    scopes = list(duc.get_lexical_scopes())
    assert len(scopes) == 1
    return scopes[0]


def test_simple() -> None:
    duc = make_duc(
        "simple",
        """\
        a = 1
        print(a + 1)
        """,
    )
    global_scope = get_global_scope(duc)

    assert_num_defs_refs(duc, global_scope, 1, 2)
    a_def = get_def(duc, global_scope, "a")
    assert isinstance(a_def.ast_node, ast.Constant)
    a_ref = get_ref(duc, global_scope, "a")
    assert len(a_ref.name_counters) == 1
    print_ref = get_ref(duc, global_scope, "print")
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
    global_scope = get_global_scope(duc)

    assert_num_defs_refs(duc, global_scope, 2, 4)

    a_def1, a_def2 = get_defs(duc, global_scope, "a", 2)
    assert a_def1.ast_node.lineno == 1
    assert a_def2.ast_node.lineno == 3

    a_ref1, a_ref2 = get_refs(duc, global_scope, "a", 2)
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
    global_scope = get_global_scope(duc)

    assert_num_defs_refs(duc, global_scope, 3, 5)

    a_def1, a_def2 = get_defs(duc, global_scope, "a", 2)
    assert a_def1.ast_node.lineno == 3
    assert a_def2.ast_node.lineno == 5

    get_refs(duc, global_scope, "b", 2)

    a_ref1, a_ref2 = get_refs(duc, global_scope, "a", 2)
    assert len(a_ref1.name_counters) == 0
    assert len(a_ref2.name_counters) == 2


def main() -> None:
    test_simple()
    test_reassign()
    test_ssa_example()


if __name__ == "__main__":
    main()
