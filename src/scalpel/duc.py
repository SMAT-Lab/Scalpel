"""
This module implements a `DUC` class for define-use chain construction.
"""

import ast
from collections import defaultdict
from dataclasses import dataclass
from itertools import groupby
from contextlib import contextmanager
import builtins
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
from scalpel.SSA.ssa import SSAConverter
from ._duc import DefUseChains, Definition, Reference, ReferencedName, Variable


'''
MODULE_SCOPE = "mod"
Builtins = {k: v for k, v in builtins.__dict__.items()}
Builtins["__file__"] = __file__


def get_arguments_names(args) ->List[str]:
    """
    return all arguments of the given ast.arguments instance.
    """
    return args.args + args.posonlyargs +args.vararg + args.kwonlyargs + args.kwarg
   

@dataclass
class Definition:
    name: str
    counter: int  # counter for SSA forms
    ast_node: ast.AST
    scope: str # scope name 
    
    __slots__ = "node", "_users", "islive"
    def add_use(self, use_node):
        """
        Add a use of the variable at a specific node.

        Args:
            use_node: The node where the variable is used.
        """
        self.uses.append(use_node)
        self.is_live: bool = True # whether this definition is live or not

    def __str__(self):
        """
        Return the string representation of the variable.
        Returns:
            str: The name of the variable.
        """
        return self.name()
    
    def is_live(self):
        # check whether this definition is live or not
        return self.is_live
    
    def name(self):
        # return the name of this definition
        if type(self.ast_node) in [ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef]:
            return self.ast_node.name 
        elif isinstance(self.node, ast.arg):
            pass 
        elif type(self.ast_node) in [ast.Import, ast.ImportFrom]:
            pass 
        elif type(self.ast_node)  == ast.alias:
            return self.ast_node.name.split(".", 1)[0]
        elif isinstance(self.ast_node.id, ast.Name):
            return self.ast_node.id
        else:
            return type(self.node).__name__


@dataclass
class ReferencedName:
    name: str
    counters: Set[int] # which numbered variable used

@dataclass
class Reference:
    name: ReferencedName
    """
    The id of the CFG block that this reference is in.
    """
    block_id: int
    """
    The index of the statement in the CFG block that this reference is in.
    """  
    stmt_idx: int

class Variable:
    """
    Represents a variable 
    Attributes:
        name (str): The name of the variable.
        idx (int):  for numbering this variable. 
        definition: The node where the variable is defined.
        uses (list): List of nodes where the variable is used. 
    """


    def __init__(self, name, count, scope):
        """
        Initialize a Variable instance.
        Args:
            name (str): The name of the variable.
        """
        self.name: str = name 
        self.count: int = count # counter for SSA forms
        self.scope: str  = scope# scope name 

        self.ast_node: Optional[ast.AST] = None 
        self.uses:List[ast.expr] = []  # usages  # experssions  
        self.type:type = any    # type for this variable 

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
    
"""
A tuple `(key, value)`. 
"""
ContainerElement = Tuple[Optional[ReferencedName], ReferencedName]

"""
A tuple `(container, element)`, where `element` is a tuple `(key, value)`. 
With this type can we describe the relationships between containers and their elements.
"""
ContainerMap = Tuple[ReferencedName, ContainerElement]

class DUC:
    """
    Definition-use chain (DUC). This class provides methods to query the definitions and references for a name in a lexical scope.
    """

    __slots__ = [ "variables", "definitions", "references"]
    def __init__(self, cfg_dict: dict[str:CFG]):
        """
        Constructs a def-use chain.
        Args:
            cfg: The control flow graph.
        """
        self.definitions:List[Definition] = [] 
        self.references:List[ReferencedName] = []
        for scope, cfg in cfg_dict.items():
            ssa_results, const_dict, loaded_value_exprs = SSAConverter().convert(cfg)
            #print(ssa_results)
            #print(const_dict)
            value_exprs_unfold  = {}
            for k, v in ssa_results.items():
                n_stmt = len(v)
                for stmt_idx in range(n_stmt):
                    expr = loaded_value_exprs[k][stmt_idx]
                    ssa_rep = v[stmt_idx]
                    for var_name, counters in ssa_rep.items():
                        for c in counters:
                            value_exprs_unfold[(var_name, c)] = expr 
                    #value_exprs_unfold.append(ssa_rep, expr)

            for (var_name, idx), val in const_dict.items():
              
                new_def = Variable(var_name, idx, scope) 
                new_def.define(val)
                # lookup its references 
                if (var_name, idx) in value_exprs_unfold:
                    used_expr = value_exprs_unfold[(var_name,idx)]
                    new_def.add_use(used_expr)
                 
                self.definitions.append(new_def)
                 # this is to check usages 
                       
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

    def iter_definitions(self, scope: str = MODULE_SCOPE) -> Iterator[Definition]:
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
        return self.references
    

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

class _ContainerRelationshipVisitor(ast.NodeVisitor):
    def __init__(self, name_to_counters: Dict[str, Set[int]]):
        self.name_to_counters = name_to_counters
        self.result: List[ContainerMap] = []

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
    


def get_duc(cfg_dict: dict[str:CFG]) -> DUC:
    """
    Constructs a def-use chain.
    Args:
        cfg: The control flow graph.
    Returns: A def-use chain.
    """
    return DUC(cfg_dict)

'''