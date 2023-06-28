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
    assert len(defs) == num_defs
    assert len(refs) == num_refs


def get_and_check_defs(duc: DUC, scope: str, name: str, num: int) -> List[Definition]:
    defs = duc.get_definitions(scope, name)
    assert len(defs) == num, f"expected {num} definitions, got {len(defs)}"
    assert all(
        def_.name == name for def_ in defs
    ), f"not all definitions have name {name}"
    return defs


def get_and_check_def(duc: DUC, scope: str, name: str) -> Definition:
    return get_and_check_defs(duc, scope, name, 1)[0]


def get_and_check_refs(duc: DUC, scope: str, name: str, num: int) -> List[Reference]:
    refs = duc.get_references(scope, name)
    assert len(refs) == num, f"expected {num} references, got {len(refs)}"
    assert all(ref.name == name for ref in refs), f"not all references have name {name}"
    return refs


def test_simple() -> None:
    duc = make_duc(
        "simple",
        """\
        a = 1
        print(a + 1)
        """,
    )

    scopes = list(duc.get_lexical_scopes())
    assert len(scopes) == 1
    global_scope = scopes[0]

    assert_num_defs_refs(duc, global_scope, 1, 1)
    a_def = get_and_check_def(duc, global_scope, "a")
    assert isinstance(a_def.ast_node, ast.Assign)
    get_and_check_refs(duc, global_scope, "a", 1)


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

    scopes = list(duc.get_lexical_scopes())
    assert len(scopes) == 2
    global_scope, f_scope = scopes

    assert_num_defs_refs(duc, global_scope, 2, 0)
    a_def = get_and_check_def(duc, global_scope, "a")
    assert isinstance(a_def.ast_node, ast.Assign)
    assert a_def.location.line == 1
    f_def = get_and_check_def(duc, global_scope, "f")
    assert isinstance(f_def.ast_node, ast.FunctionDef)

    assert_num_defs_refs(duc, f_scope, 2, 0)
    f_a_def = get_and_check_def(duc, f_scope, "a")
    assert isinstance(f_a_def.ast_node, ast.Assign)
    assert f_a_def.location.line == 3
    f_b_def = get_and_check_def(duc, f_scope, "b")
    assert isinstance(f_b_def.ast_node, ast.Assign)


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

    scopes = list(duc.get_lexical_scopes())
    assert len(scopes) == 1
    global_scope = scopes[0]

    assert_num_defs_refs(duc, global_scope, 2, 2)

    a_def1, a_def2 = get_and_check_defs(duc, global_scope, "a", 2)
    assert a_def1.location.line == 1
    assert a_def2.location.line == 3

    a_ref1, a_ref2 = get_and_check_refs(duc, global_scope, "a", 2)
    assert a_ref1.location.line == 2
    assert a_ref2.location.line == 4


def test_classes() -> None:
    duc = make_duc(
        "classes",
        """\
        a = 1
        class C:
            a = 2
            b = a
            def f(self):
                print(a)
                print(b)
        print(a)
        """,
    )

    scopes = list(duc.get_lexical_scopes())
    assert len(scopes) == 3
    global_scope, c_scope, c_f_scope = scopes

    assert_num_defs_refs(duc, global_scope, 1, 1)
    assert get_and_check_def(duc, global_scope, "a").location.line == 1
    global_a_ref1, global_a_ref2 = get_and_check_refs(duc, global_scope, "a", 2)
    assert global_a_ref1.location.line == 6  # print(a) inside C.f
    assert global_a_ref2.location.line == 8  # print(a) in global scope

    assert_num_defs_refs(duc, c_scope, 2, 1)
    a_def = get_and_check_def(duc, c_scope, "a")
    assert a_def.location.line == 3
    a_ref = get_and_check_refs(duc, c_scope, "a", 1)[0]
    assert a_ref.location.line == 4  # b = a

    assert_num_defs_refs(duc, c_f_scope, 1, 2)
    self_def = get_and_check_def(duc, c_f_scope, "self")
    assert isinstance(self_def.ast_node, ast.arg)


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

    scopes = list(duc.get_lexical_scopes())
    assert len(scopes) == 2
    global_scope, f_scope = scopes[0]

    assert_num_defs_refs(duc, global_scope, 3, 0)
    global_a_def1, global_a_def2 = get_and_check_defs(duc, global_scope, "a", 2)
    assert isinstance(global_a_def1.ast_node, ast.Assign)
    assert isinstance(global_a_def2.ast_node, ast.For)
    f_def = get_and_check_def(duc, global_scope, "f")
    assert isinstance(f_def, ast.FunctionDef)
    get_and_check_refs(duc, global_scope, "a", 0)

    assert_num_defs_refs(duc, f_scope, 2, 2)
    assert isinstance(get_and_check_def(duc, f_scope, "a").ast_node, ast.arg)
    assert isinstance(get_and_check_def(duc, f_scope, "b").ast_node, ast.arg)


def main() -> None:
    test_simple()
    test_multiple_scopes()
    test_reassign()
    test_classes()
    test_multiple_defs()


if __name__ == "__main__":
    main()
