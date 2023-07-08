"""
This module implements a `DUC` class for define-use chain construction.
"""

import ast
from dataclasses import dataclass
from typing import (
    Dict,
    Iterator,
    List,
    Set,
    Tuple,
    Union,
)
from scalpel.cfg import CFG
from scalpel.SSA.const import SSA
from scalpel.cfg.builder import CFGBuilder


@dataclass
class Definition:
    name: str
    counter: int
    ast_node: ast.AST


@dataclass
class Reference:
    name: str
    block_id: int
    """
    The id of the CFG block that this reference is in.
    """
    stmt_idx: int
    """
    The index of the statement in the CFG block that this reference is in.
    """
    name_counters: Set[int]


Scope = Union[Tuple[int, str], str, None]
"""
Either
- a tuple (block_id, name), representing a function lexical scope where block_id
  is the id of the block in the CFG that the function is in
- a string, representing the name of a class
- None, representing the global scope
"""


class DUC:
    """
    Definition-use chain (DUC). This class provides methods to query the
    definitions and references for a name in a lexical scope.
    """

    __slots__ = [
        "cfg",
        "ssa_results",
        "const_dict",
        "function_ducs",
        "class_ducs",
    ]

    def __init__(self, cfg: CFG):
        """
        Constructs a def-use chain.
        Args:
            cfg: The control flow graph.
        """
        self.cfg = cfg
        ssa_results, const_dict = SSA().compute_SSA(cfg)
        self.ssa_results = ssa_results
        self.const_dict = const_dict
        self.function_ducs: Dict[Tuple[int, str], DUC] = {}
        self.class_ducs: Dict[str, DUC] = {}

    def get_function_scopes(self) -> Iterator[Tuple[int, str]]:
        """
        Iterates the names of all the function lexical scopes.
        Returns: An iterator of the lexical scope names (tuples of (block_id, name)).
        """
        yield from self.cfg.functioncfgs

    def get_class_scopes(self) -> Iterator[str]:
        """
        Iterates the names of all the class lexical scopes.
        Returns: An iterator of the lexical scope names (strings).
        """
        yield from self.cfg.class_cfgs

    def get_lexical_scopes(self) -> Iterator[Scope]:
        """
        Iterates the names of all the lexical scopes.
        Returns: An iterator of the lexical scope names. The iterator will yield
        all the function lexical scopes, then all the class lexical scopes.
        """

        def get_scopes(scope: Scope, cfg: CFG) -> Iterator[Scope]:
            yield scope
            for scope, cfg in cfg.functioncfgs.items():
                yield from get_scopes(scope, cfg)
            for scope, cfg in cfg.class_cfgs.items():
                yield from get_scopes(scope, cfg)

        return get_scopes(None, self.cfg)

    def get_definitions_and_references(
        self, scope: Scope = None
    ) -> Tuple[List[Definition], List[Reference]]:
        """
        Retrieves all the definitions and references for a lexical scope.
        Args:
            scope: The lexical scope. `None` refers to the global scope.
        Returns:
            A tuple of `(definitions, references)`. `definitions` is a list of
            all the definitions (AST nodes) in the lexical scope `scope`,
            and `references` is a list of all the references (AST nodes) in the
            scope.
        """
        if scope is None:
            return (
                [
                    Definition(name, counter, value)
                    for (name, counter), value in self.const_dict.items()
                ],
                [
                    Reference(name, block_id, stmt_idx, counters)
                    for block_id, stmts in self.ssa_results.items()
                    for stmt_idx, stmt in enumerate(stmts)
                    for name, counters in stmt.items()
                ],
            )
        return self._apply_to_child_ducs(scope, DUC.get_definitions_and_references) or (
            [],
            [],
        )

    def get_definitions(self, var_name: str, scope: Scope = None) -> List[Definition]:
        """
        Retrieves the definitions for a variable in a lexical scope.
        Args:
            var_name: The name of the variable (string).
            scope: The lexical scope. `None` refers to the global scope.
        Returns: A list of definitions.
        """
        if scope is None:
            return [
                Definition(name, counter, value)
                for (name, counter), value in self.const_dict.items()
                if name == var_name
            ]
        return self._apply_to_child_ducs(scope, DUC.get_definitions, var_name) or []

    def get_references(self, var_name: str, scope: Scope = None) -> List[Reference]:
        """
        Retrieves the references for a variable in a lexical scope.
        Args:
            var_name: The name of the variable (string).
            scope: The lexical scope. `None` refers to the global scope.
        Returns: A list of references.
        """
        if scope is None:
            return [
                Reference(name, block_id, stmt_idx, counters)
                for block_id, stmts in self.ssa_results.items()
                for stmt_idx, stmt in enumerate(stmts)
                for name, counters in stmt.items()
                if name == var_name
            ]
        return self._apply_to_child_ducs(scope, DUC.get_references, var_name) or []

    def ast_node_for_reference(self, reference: Reference) -> ast.stmt:
        """
        Retrieves the AST node for a reference from this DUC.
        Args:
            reference: The reference. This must be a valid reference from this
            DUC.
        Returns: An AST statement node.
        """
        return next(
            block.statements[reference.stmt_idx]
            for block in self.cfg
            if block.id == reference.block_id
        )

    def duc_for_function(self, scope: Tuple[int, str]) -> "DUC":
        """
        Retrieves a def-use chain for a function.
        Args:
            scope: A tuple (block_id, name) of the function, where block_id is
            the id of the CFG block that the function is in. This must be a
            valid scope (for example returned from `get_function_scopes`).
        Returns: A DUC.
        """
        if scope not in self.function_ducs:
            self.function_ducs[scope] = DUC(self.cfg.functioncfgs[scope])
        return self.function_ducs[scope]

    def duc_for_class(self, scope: str) -> "DUC":
        """
        Retrieves a def-use chain for a class.
        Args:
            scope: The name of the class (string) This must be a valid scope
            (for example returned from `get_class_scopes`).
        Returns: A DUC.
        """
        if scope not in self.class_ducs:
            self.class_ducs[scope] = DUC(self.cfg.class_cfgs[scope])
        return self.class_ducs[scope]

    def get_all_ducs(self) -> Iterator["DUC"]:
        """
        Iterates the DUCs of the lexical scopes in this CFG.
        """
        yield self
        for scope in self.get_function_scopes():
            yield from self.duc_for_function(scope).get_all_ducs()
        for scope in self.get_class_scopes():
            yield from self.duc_for_class(scope).get_all_ducs()

    # _apply_to_child_ducs(self, scope: Scope, fn: Callable[[DUC, *A], T], *args: *A) -> T | None
    def _apply_to_child_ducs(self, scope: Scope, fn, *args):
        if isinstance(scope, str):
            if scope in self.cfg.class_cfgs:
                return fn(self.duc_for_class(scope), *args)
        else:
            if scope in self.cfg.functioncfgs:
                return fn(self.duc_for_function(scope), *args)


def ducs_from_src(name: str, src: str) -> Iterator[DUC]:
    return DUC(CFGBuilder().build_from_src(name, src)).get_all_ducs()
