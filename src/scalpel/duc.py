"""
This module implements a `DUC` class for define-use chain construction.
"""

import ast
from dataclasses import dataclass
import sys
from typing import Iterable, List, NoReturn, Tuple, Union
from scalpel.cfg import CFG


@dataclass
class Location:
    """
    A location within a source file.
    """

    line: int
    """
    The line (first line is 1).
    """

    column: int
    """
    The column offset (first character in the line is 0).
    """


@dataclass
class Definition:
    name: str
    location: Location
    ast_node: Union[
        ast.AnnAssign,
        ast.Assign,
        ast.AugAssign,
        ast.AsyncFor,
        ast.AsyncFunctionDef,
        ast.ExceptHandler,
        ast.FunctionDef,
        ast.ClassDef,
        ast.For,
        # imports
        ast.alias,
        ast.arg,
        ast.comprehension,
        ast.withitem,
        # walrus operator
        (ast.NamedExpr if sys.version_info >= (3, 8) else NoReturn),
        # match patterns
        (ast.MatchAs if sys.version_info >= (3, 10) else NoReturn),
    ]


@dataclass
class Reference:
    name: str
    location: Location
    ast_node: ast.Name


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
        pass

    def get_lexical_scopes(self) -> Iterable[str]:
        """
        Iterates the names of all the lexical scopes.
        Returns: An iterable of the lexical scope names (strings).
        """
        pass

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
        pass

    def get_definitions(self, scope_name: str, name: str) -> List[Definition]:
        """
        Retrieves the definitions for a variable in a lexical scope.
        Args:
            scope_name: The name of the lexical scope (string).
            name: The name of the variable (string).
        Returns: A list of definitions (AST nodes).
        """
        pass

    def get_references(self, scope_name: str, name: str) -> List[Reference]:
        """
        Retrieves the references for a variable in a lexical scope.
        Args:
            scope_name: The name of the lexical scope (string).
            name: The name of the variable (string).
        Returns: A list of references (AST nodes).
        """
        pass
