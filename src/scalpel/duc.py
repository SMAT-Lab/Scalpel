"""
This module implements a `DUC` class for define-use chain construction.
"""

import ast
from collections import defaultdict
from dataclasses import dataclass
from itertools import groupby
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
from scalpel.cfg import CFG
from scalpel.SSA.const import SSA

MODULE_SCOPE = "mod"


class Variable:
    """
    Represents a variable 
    Attributes:
        name (str): The name of the variable.
        idx (int):  for numbering this variable. 
        definition: The node where the variable is defined.
        uses (list): List of nodes where the variable is used. 
    """

    def __init__(self, name, idx):
        """
        Initialize a Variable instance.
        Args:
            name (str): The name of the variable.
        """
        self.name:str = name
        self.idx:int = idx  # numbers 
        self.definition = None
        self.uses:List[ast.expr] = []  # usages  # experssions  
        self.value:ast.expr  = None  # for context sensitive analysis.
        self.type:type = any    # type for this variable 
        self.scope_name:str = None  # the lexical scope it is defined 

    def define(self, definition_node):
        """
        Define the variable at a specific node.
        Args:
            definition_node: The node where the variable is defined.
        """
        self.definition = definition_node

    def add_use(self, use_node):
        """
        Add a use of the variable at a specific node.

        Args:
            use_node: The node where the variable is used.
        """
        self.uses.append(use_node)

    def __str__(self):
        """
        Return the string representation of the variable.

        Returns:
            str: The name of the variable.
        """
        return self.name

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

        self.variables = {}

    def get_or_create_variable(self, var_name):
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            new_variable = Variable(var_name)
            self.variables[var_name] = new_variable
            return new_variable

    def add_definition(self, var_name, definition_node):
        variable = self.get_or_create_variable(var_name)
        variable.define(definition_node)

    def add_use(self, var_name, use_node):
        variable = self.get_or_create_variable(var_name)
        variable.add_use(use_node)

    def get_variable(self, var_name):
        return self.variables.get(var_name)

    def __str__(self):
        result = ""
        for var_name, variable in self.variables.items():
            result += f"{var_name}:\n"
            if variable.definition:
                result += f"  Definition: {variable.definition}\n"
            if variable.uses:
                result += "  Uses: " + ", ".join(str(use) for use in variable.uses) + "\n"
        return result

    def get_lexical_scopes(self) -> Iterator[str]:
        """
        Iterates the names of all the lexical scopes.
        Returns: An iterator of the lexical scope names.
        """
        yield from self.cfgs

    def get_all_definitions(self, scope: str = MODULE_SCOPE) -> Iterator[Definition]:
        """
        Retrieves the definitions for a variable in a lexical scope.
        Args:
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: A iterator of definitions.
        """
        for (name, counter), value in self.const_dicts[scope].items():
            yield Definition(name, counter, value)

    def get_all_references(self, scope: str = MODULE_SCOPE) -> Iterator[Reference]:
        """
        Retrieves the references for a variable in a lexical scope.
        Args:
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: An iterator of references.
        """
        for block_id, stmts in self.ssa_results[scope].items():
            for stmt_idx, stmt in enumerate(stmts):
                for name, counters in stmt.items():
                    yield Reference(ReferencedName(name, counters), block_id, stmt_idx)

    def get_all_definitions_and_references(
        self, scope: str = MODULE_SCOPE
    ):
        """
        Retrieves all the definitions and references for a lexical scope.
        Args:
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns:
            A tuple of `(definitions, references)`. `definitions` is an iterator
            of all the definitions (AST nodes) in the lexical scope `scope`, and
            `references` is a iterator of all the references (AST nodes) in the
            scope.
        """
        return self.get_all_definitions(scope), self.get_all_references(scope)

    def get_definitions(
        self, name: str, scope: str = MODULE_SCOPE
    ):
        """
        Retrieves all the definitions in a lexical scope.
        Args:
            name: The name of the variable (string).
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: An iterator of definitions.
        """
        for definition in self.get_all_definitions(scope):
            if definition.name == name:
                yield definition

    def get_references(
        self, name: str, scope: str = MODULE_SCOPE
    ):
        """
        Retrieves all the references in a lexical scope.
        Args:
            name: The name of the variable (string).
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: An iterator of references.
        """
        for reference in self.get_all_references(scope):
            if reference.name.name == name:
                yield reference

    def ast_node_for_reference(
        self, reference, scope: str = MODULE_SCOPE
    ) -> ast.stmt:
        """
        Retrieves the AST node for a reference from this DUC.
        Args:
            reference: The reference. This must be a valid reference from this
            DUC.
            scope: The name of the scope (defaults to `"mod"`, the scope of the
            module).
        Returns: An AST statement node.
        """
        return self._ast_node(scope, reference.block_id, reference.stmt_idx)

    def container_relationships(self, scope: str = MODULE_SCOPE):
        for (block_id, stmt_idx), references in groupby(
            self.get_all_references(scope), lambda ref: (ref.block_id, ref.stmt_idx)
        ):
            name_to_counters: Dict[str, Set[int]] = defaultdict(set)
            for ref in references:
                name_to_counters[ref.name.name] |= ref.name.counters
            visitor = _ContainerRelationshipVisitor(name_to_counters)
            visitor.visit(self._ast_node(scope, block_id, stmt_idx))
            yield from visitor.result

    def _ast_node(self, scope: str, block_id: int, stmt_idx: int) -> ast.stmt:
        return next(
            block.statements[stmt_idx]
            for block in self.cfgs[scope]
            if block.id == block_id
        )

#Example usage
#def_use_chain = DefUseChain()
#def_use_chain.add_definition("x", "x = 10")
#def_use_chain.add_use("x", "print(x)")
#def_use_chain.add_use("x", "y = x + 5")
#def_use_chain.add_definition("y", "y = x * 2")
#def_use_chain.add_use("y", "z = y - 3")


@dataclass
class Definition:
    name: str
    counter: int
    ast_node: ast.AST


@dataclass
class ReferencedName:
    name: str
    counters: Set[int]


@dataclass
class Reference:
    name: ReferencedName
    block_id: int
    """
    The id of the CFG block that this reference is in.
    """
    stmt_idx: int
    """
    The index of the statement in the CFG block that this reference is in.
    """

ContainerElement = Tuple[Optional[ReferencedName], ReferencedName]
"""
A tuple `(key, value)`.
"""

ContainerRelationship = Tuple[ReferencedName, ContainerElement]
"""
A tuple `(container, element)`, where `element` is a tuple `(key, value)`.
"""


class _ContainerRelationshipVisitor(ast.NodeVisitor):
    def __init__(self, name_to_counters: Dict[str, Set[int]]):
        self.name_to_counters = name_to_counters
        self.result: List[ContainerRelationship] = []

    def visit_Assign(self, node) -> None:
        self._visit_assign(node.targets, node.value)

    def visit_AnnAssign(self, node) -> None:
        if node.value:
            self._visit_assign((node.target,), node.value)

    def visit_AugAssign(self, node) -> None:
        if not isinstance(node.target, ast.Name):
            return
        container = self._name(node.target)
        # container += [value]
        # container |= {value}
        if (
            isinstance(node.op, ast.Add)
            and isinstance(node.value, ast.List)
            or isinstance(node.op, ast.BitOr)
            and isinstance(node.value, ast.Set)
        ):
            self.result.extend(
                (container, elt) for elt in self._list_elements(node.value)
            )
        # container |= {key: value}
        elif isinstance(node.op, ast.BitOr) and isinstance(node.value, ast.Dict):
            self.result.extend(
                (container, elt) for elt in self._dict_elements(node.value)
            )

    def visit_Call(self, node) -> None:
        if not (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
        ):
            return
        container = self._name(node.func.value)
        # container.add(value)
        if (
            (
                node.func.attr == "add"
                or node.func.attr == "append"
                or node.func.attr == "appendleft"
            )
            and len(node.args) == 1
            and isinstance(node.args[0], ast.Name)
            and not node.keywords
        ):
            self.result.append((container, (None, self._name(node.args[0]))))
        # container.insert(i, value)
        elif (
            node.func.attr == "insert"
            and len(node.args) == 2
            and not isinstance(node.args[0], ast.Starred)
            and isinstance(node.args[1], ast.Name)
            and not node.keywords
        ):
            self.result.append((container, (None, self._name(node.args[1]))))
        # container.update({key: value}, key=value)
        elif node.func.attr == "update" and (
            not node.args or len(node.args) == 1 and isinstance(node.args[0], ast.Dict)
        ):
            if node.args:
                self.result.extend(
                    (container, elt) for elt in self._dict_elements(node.args[0])
                )
            self.result.extend(
                (container, (None, self._name(keyword.value)))
                for keyword in node.keywords
                if isinstance(keyword.value, ast.Name)
            )

    def _visit_assign(self, targets: Iterable[ast.expr], expr: ast.expr) -> None:
        def extend(elements: Iterable[ContainerElement]) -> None:
            elts = list(elements)
            self.result.extend(
                (self._name(target), elt)
                for target in targets
                if isinstance(target, ast.Name)
                for elt in elts
            )

        if isinstance(expr, ast.Name):
            value = self._name(expr)
            self.result.extend(
                (
                    self._name(target.value),
                    (self._name(target.slice), value),
                )
                for target in targets
                if isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and isinstance(target.slice, ast.Name)
            )

        # container = [value]
        # container = {value}
        elif isinstance(expr, (ast.List, ast.Set)):
            extend(self._list_elements(expr))
        # container = {key: value}
        elif isinstance(expr, ast.Dict):
            extend(self._dict_elements(expr))
        elif isinstance(expr, ast.BinOp):
            # container = [value] + [value]
            if isinstance(expr.op, ast.Add):
                extend(
                    elt
                    for expr in (expr.left, expr.right)
                    for elt in (
                        self._list_elements(expr) if isinstance(expr, ast.List) else ()
                    )
                )
            # container = {value} | {value}
            # container = {key: value} | {key: value}
            elif isinstance(expr.op, ast.BitOr):
                extend(
                    elt
                    for expr in (expr.left, expr.right)
                    for elt in (
                        self._list_elements(expr)
                        if isinstance(expr, ast.Set)
                        else (
                            self._dict_elements(expr)
                            if isinstance(expr, ast.Dict)
                            else ()
                        )
                    )
                )

    def _dict_elements(self, dct: ast.Dict) -> Iterator[ContainerElement]:
        for key, value in zip(dct.keys, dct.values):
            if isinstance(value, ast.Name):
                yield (
                    self._name(key) if isinstance(key, ast.Name) else None,
                    self._name(value),
                )

    def _list_elements(
        self, lst: Union[ast.List, ast.Set]
    ) -> Iterator[ContainerElement]:
        for elt in lst.elts:
            if isinstance(elt, ast.Name):
                yield None, self._name(elt)

    def _name(self, name: ast.Name) -> ReferencedName:
        return ReferencedName(name.id, self.name_to_counters[name.id])
