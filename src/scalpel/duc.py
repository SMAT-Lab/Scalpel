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
)
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


MODULE_SCOPE = "mod"

class DUC:
    """
    Definition-use chain (DUC). This class provides methods to query the
    definitions and references for a name in a lexical scope.
    """

    __slots__ = [
        "cfgs",
        "ssa_results",
        "const_dicts",
    ]

    def __init__(self, cfg: CFG):
        """
        Constructs a def-use chain.
        Args:
            cfg: The control flow graph.
        """
        self.cfgs = cfg.flatten()
        self.ssa_results: Dict[str, Dict[int, List[Dict[str, Set[int]]]]] = {}
        self.const_dicts: Dict[str, Dict[Tuple[str, int], ast.AST]] = {}
        for scope, cfg in self.cfgs.items():
            ssa_results, const_dict = SSA().compute_SSA(cfg)
            self.ssa_results[scope] = ssa_results
            self.const_dicts[scope] = const_dict

    def get_lexical_scopes(self) -> Iterator[str]:
        """
        Iterates the names of all the lexical scopes.
        Returns: An iterator of the lexical scope names.
        """
        yield from self.cfgs

    def get_definitions_and_references(
        self, scope: str = MODULE_SCOPE
    ) -> Tuple[List[Definition], List[Reference]]:
        """
        Retrieves all the definitions and references for a lexical scope.
        Args:
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns:
            A tuple of `(definitions, references)`. `definitions` is a list of
            all the definitions (AST nodes) in the lexical scope `scope`,
            and `references` is a list of all the references (AST nodes) in the
            scope.
        """
        return (
            [
                Definition(name, counter, value)
                for (name, counter), value in self.const_dicts[scope].items()
            ],
            [
                Reference(name, block_id, stmt_idx, counters)
                for block_id, stmts in self.ssa_results[scope].items()
                for stmt_idx, stmt in enumerate(stmts)
                for name, counters in stmt.items()
            ],
        )

    def get_definitions(self, var_name: str, scope: str = MODULE_SCOPE) -> List[Definition]:
        """
        Retrieves the definitions for a variable in a lexical scope.
        Args:
            var_name: The name of the variable (string).
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: A list of definitions.
        """
        return [
            Definition(name, counter, value)
            for (name, counter), value in self.const_dicts[scope].items()
            if name == var_name
        ]

    def get_references(self, var_name: str, scope: str = MODULE_SCOPE) -> List[Reference]:
        """
        Retrieves the references for a variable in a lexical scope.
        Args:
            var_name: The name of the variable (string).
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: A list of references.
        """
        return [
            Reference(name, block_id, stmt_idx, counters)
            for block_id, stmts in self.ssa_results[scope].items()
            for stmt_idx, stmt in enumerate(stmts)
            for name, counters in stmt.items()
            if name == var_name
        ]

    def ast_node_for_reference(self, reference: Reference, scope: str = MODULE_SCOPE) -> ast.stmt:
        """
        Retrieves the AST node for a reference from this DUC.
        Args:
            reference: The reference. This must be a valid reference from this
            DUC.
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: An AST statement node.
        """
        return next(
            block.statements[reference.stmt_idx]
            for block in self.cfgs[scope]
            if block.id == reference.block_id
        )
