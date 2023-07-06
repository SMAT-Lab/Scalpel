"""
This module implements a `DUC` class for define-use chain construction.
"""

import ast
from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple
from scalpel.cfg import CFG
from scalpel.SSA.const import SSA


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


GLOBAL_SCOPE = "GLOBAL"


class DUC:
    """
    Definition-use chain (DUC). This class provides methods to query the
    definitions and references for a name in a lexical scope.
    """

    def __init__(self, cfg: CFG):
        """
        Constructs a def-use chain.
        Args:
            cfg: The control flow graph.
        """
        ssa_results, const_dict = SSA().compute_SSA(cfg)
        self.ssa_results = ssa_results
        self.const_dict = const_dict

    def get_lexical_scopes(self) -> Iterable[str]:
        """
        Iterates the names of all the lexical scopes.
        Returns: An iterable of the lexical scope names (strings).
        """
        yield GLOBAL_SCOPE

    def get_definitions_and_references(
        self, scope_name: str
    ) -> Tuple[List[Definition], List[Reference]]:
        """
        Retrieves all the definitions and references for a lexical scope.
        Args:
            scope_name: The name of the lexical scope (string).
        Returns:
            A tuple of `(definitions, references)`. `definitions` is a list of
            all the definitions (AST nodes) in the lexical scope `scope_name`,
            and `references` is a list of all the references (AST nodes) in the
            scope.
        """
        return (
            (
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
            if scope_name == GLOBAL_SCOPE
            else ([], [])
        )

    def get_definitions(self, scope_name: str, var_name: str) -> List[Definition]:
        """
        Retrieves the definitions for a variable in a lexical scope.
        Args:
            scope_name: The name of the lexical scope (string).
            name: The name of the variable (string).
        Returns: A list of definitions.
        """
        return (
            [
                Definition(name, counter, value)
                for (name, counter), value in self.const_dict.items()
                if name == var_name
            ]
            if scope_name == GLOBAL_SCOPE
            else []
        )

    def get_refs(self, scope_name: str, var_name: str) -> List[Reference]:
        """
        Retrieves the references for a variable in a lexical scope.
        Args:
            scope_name: The name of the lexical scope (string).
            name: The name of the variable (string).
        Returns: A list of references.
        """
        return (
            [
                Reference(name, block_id, stmt_idx, counters)
                for block_id, stmts in self.ssa_results.items()
                for stmt_idx, stmt in enumerate(stmts)
                for name, counters in stmt.items()
                if name == var_name
            ]
            if scope_name == GLOBAL_SCOPE
            else []
        )
