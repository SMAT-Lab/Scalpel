"""
This module implements a `DUC` class for define-use chain construction.
"""

import ast
from collections import defaultdict
from dataclasses import dataclass
from itertools import groupby
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


## This implementation is based on the original implementation of DefUseChains in [beniget](https://github.com/serge-sans-paille/beniget/blob/master/beniget/beniget.py)
class DefUseChains(ast.NodeVisitor):
    """
    Module visitor that gathers two kinds of informations:
        - locals: Dict[node, List[Def]], a mapping between a node and the list
          of variable defined in this node,
        - chains: Dict[node, Def], a mapping between nodes and their chains.

    >>> import gast as ast
    >>> module = ast.parse("from b import c, d; c()")
    >>> duc = DefUseChains()
    >>> duc.visit(module)
    >>> for head in duc.locals[module]:
    ...     print("{}: {}".format(head.name(), len(head.users())))
    c: 1
    d: 0
    >>> alias_def = duc.chains[module.body[0].names[0]]
    >>> print(alias_def)
    c -> (c -> (Call -> ()))

    One instance of DefUseChains is only suitable to analyse one AST Module in it's lifecycle.
    """

    def __init__(self, filename=None):
        """
            - filename: str, included in error messages if specified
        """
        self.chains = {}
        self.locals = defaultdict(list)

        self.filename = filename

        # deep copy of builtins, to remain reentrant
        self._builtins = {k: Def(v) for k, v in Builtins.items()}

        # function body are not executed when the function definition is met
        # this holds a list of the functions met during body processing
        self._defered = []

        # stack of mapping between an id and Names
        self._definitions = []

        # stack of scope depth
        self._scope_depths = []

        # stack of variable defined with the global keywords
        self._globals = []

        # stack of local identifiers, used to detect 'read before assign'
        self._precomputed_locals = []

        # stack of variable that were undefined when we met them, but that may
        # be defined in another path of the control flow (esp. in loop)
        self._undefs = []

        # stack of nodes starting a scope: class, module, function, generator expression, comprehension...
        self._scopes = []

        self._breaks = []
        self._continues = []

        # stack of list of annotations (annotation, heads, callback),
        # only used in the case of from __future__ import annotations feature.
        # the annotations are analyzed when the whole module has been processed,
        # it should be compatible with PEP 563, and minor changes are required to support PEP 649.
        self._defered_annotations = []

        # dead code levels, it's non null for code that cannot be executed
        self._deadcode = 0

        # attributes set in visit_Module
        self.module = None
        self.future_annotations = False

    #
    ## helpers
    #
    def _dump_locals(self, node, only_live=False):
        """
        Like `dump_definitions` but returns the result grouped by symbol name and it includes linenos.

        :Returns: List of string formatted like: '{symbol name}:{def lines}'
        """
        groupped = defaultdict(list)
        for d in self.locals[node]:
            if not only_live or d.islive:
                groupped[d.name()].append(d)
        return ['{}:{}'.format(name, ','.join([str(getattr(d.node, 'lineno', -1)) for d in defs])) \
            for name,defs in groupped.items()]

    def dump_definitions(self, node, ignore_builtins=True):
        if isinstance(node, ast.Module) and not ignore_builtins:
            builtins = {d for d in self._builtins.values()}
            return sorted(d.name()
                          for d in self.locals[node] if d not in builtins)
        else:
            return sorted(d.name() for d in self.locals[node])

    def dump_chains(self, node):
        chains = []
        for d in self.locals[node]:
            chains.append(str(d))
        return chains

    def location(self, node):
        if hasattr(node, "lineno"):
            filename = "{}:".format(
                "<unknown>" if self.filename is None else self.filename
            )
            return " at {}{}:{}".format(filename,
                                            node.lineno,
                                            node.col_offset)
        else:
            return ""

    def unbound_identifier(self, name, node):
        self.warn("unbound identifier '{}'".format(name), node)
    
    def warn(self, msg, node):
        print("W: {}{}".format(msg, self.location(node)))

    def invalid_name_lookup(self, name, scope, precomputed_locals, local_defs):
        # We may hit the situation where we refer to a local variable which is
        # not bound yet. This is a runtime error in Python, so we try to detec
        # it statically.

        # not a local variable => fine
        if name not in precomputed_locals:
            return

        # It's meant to be a local, but can we resolve it by a local lookup?
        islocal = any((name in defs or '*' in defs) for defs in local_defs)

        # At class scope, it's ok to refer to a global even if we also have a
        # local definition for that variable. Stated other wise
        #
        # >>> a = 1
        # >>> def foo(): a = a
        # >>> foo() # fails, a is a local referenced before being assigned
        # >>> class bar: a = a
        # >>> bar() # ok, and `bar.a is a`
        if isinstance(scope, ast.ClassDef):
            top_level_definitions = self._definitions[0:-self._scope_depths[0]]
            isglobal = any((name in top_lvl_def or '*' in top_lvl_def)
                           for top_lvl_def in top_level_definitions)
            return not islocal and not isglobal
        else:
            return not islocal

    def compute_annotation_defs(self, node, quiet=False):
        name = node.id
        # resolving an annotation is a bit different
        # form other names.
        try:
            return lookup_annotation_name_defs(name, self._scopes, self.locals)
        except LookupError:
            # fallback to regular behaviour on module scope
            # to support names from builtins or wildcard imports.
            return self.compute_defs(node, quiet=quiet)

    def compute_defs(self, node, quiet=False):
        '''
        Performs an actual lookup of node's id in current context, returning
        the list of def linked to that use.
        '''
        name = node.id
        stars = []

        # If the `global` keyword has been used, honor it
        if any(name in _globals for _globals in self._globals):
            looked_up_definitions = self._definitions[0:-self._scope_depths[0]]
        else:
            # List of definitions to check. This includes all non-class
            # definitions *and* the last definition. Class definitions are not
            # included because they require fully qualified access.
            looked_up_definitions = []

            scopes_iter = iter(reversed(self._scopes))
            depths_iter = iter(reversed(self._scope_depths))
            precomputed_locals_iter = iter(reversed(self._precomputed_locals))

            # Keep the last scope because we could be in class scope, in which
            # case we don't need fully qualified access.
            lvl = depth = next(depths_iter)
            precomputed_locals = next(precomputed_locals_iter)
            base_scope = next(scopes_iter)
            defs = self._definitions[depth:]
            if not self.invalid_name_lookup(name, base_scope, precomputed_locals, defs):
                looked_up_definitions.extend(reversed(defs))

                # Iterate over scopes, filtering out class scopes.
                for scope, depth, precomputed_locals in zip(scopes_iter,
                                                            depths_iter,
                                                            precomputed_locals_iter):
                    if not isinstance(scope, ast.ClassDef):
                        defs = self._definitions[lvl + depth: lvl]
                        if self.invalid_name_lookup(name, base_scope, precomputed_locals, defs):
                            looked_up_definitions.append(StopIteration)
                            break
                        looked_up_definitions.extend(reversed(defs))
                    lvl += depth

        for defs in looked_up_definitions:
            if defs is StopIteration:
                break
            elif name in defs:
                return defs[name] if not stars else stars + list(defs[name])
            elif "*" in defs:
                stars.extend(defs["*"])

        d = self.chains.setdefault(node, Def(node))

        if self._undefs:
            self._undefs[-1][name].append((d, stars))

        if stars:
            return stars + [d]
        else:
            if not self._undefs and not quiet:
                self.unbound_identifier(name, node)
            return [d]

    defs = compute_defs

    def process_body(self, stmts):
        deadcode = False
        for stmt in stmts:
            self.visit(stmt)
            if isinstance(stmt, (ast.Break, ast.Continue, ast.Raise)):
                if not deadcode:
                    deadcode = True
                    self._deadcode += 1
        if deadcode:
            self._deadcode -= 1

    def process_undefs(self):
        for undef_name, _undefs in self._undefs[-1].items():
            if undef_name in self._definitions[-1]:
                for newdef in self._definitions[-1][undef_name]:
                    for undef, _ in _undefs:
                        for user in undef.users():
                            newdef.add_user(user)
            else:
                for undef, stars in _undefs:
                    if not stars:
                        self.unbound_identifier(undef_name, undef.node)
        self._undefs.pop()

    @contextmanager
    def ScopeContext(self, node):
        self._scopes.append(node)
        self._scope_depths.append(-1)
        self._definitions.append(defaultdict(ordered_set))
        self._globals.append(set())
        self._precomputed_locals.append(collect_locals(node))
        yield
        self._precomputed_locals.pop()
        self._globals.pop()
        self._definitions.pop()
        self._scope_depths.pop()
        self._scopes.pop()

    if sys.version_info.major >= 3:
        CompScopeContext = ScopeContext
    else:
        @contextmanager
        def CompScopeContext(self, node):
            yield


    @contextmanager
    def DefinitionContext(self, definitions):
        self._definitions.append(definitions)
        self._scope_depths[-1] -= 1
        yield self._definitions[-1]
        self._scope_depths[-1] += 1
        self._definitions.pop()


    @contextmanager
    def SwitchScopeContext(self, defs, scopes, scope_depths, precomputed_locals):
        scope_depths, self._scope_depths = self._scope_depths, scope_depths
        scopes, self._scopes = self._scopes, scopes
        defs, self._definitions = self._definitions, defs
        precomputed_locals, self._precomputed_locals = self._precomputed_locals, precomputed_locals
        yield
        self._definitions = defs
        self._scopes = scopes
        self._scope_depths = scope_depths
        self._precomputed_locals = precomputed_locals

    def process_functions_bodies(self):
        for fnode, defs, scopes, scope_depths, precomputed_locals in self._defered:
            visitor = getattr(self,
                              "visit_{}".format(type(fnode).__name__))
            with self.SwitchScopeContext(defs, scopes, scope_depths, precomputed_locals):
                visitor(fnode, step=DefinitionStep)

    def process_annotations(self):
        compute_defs, self.defs = self.defs,  self.compute_annotation_defs
        for annnode, heads, cb in self._defered_annotations[-1]:
            visitor = getattr(self,
                                "visit_{}".format(type(annnode).__name__))
            currenthead, self._scopes = self._scopes, heads
            cb(visitor(annnode)) if cb else visitor(annnode)
            self._scopes = currenthead
        self.defs = compute_defs

    # stmt
    def visit_Module(self, node):
        self.module = node

        futures = collect_future_imports(node)
        # determine whether the PEP563 is enabled
        # allow manual enabling of DefUseChains.future_annotations
        self.future_annotations |= 'annotations' in futures


        with self.ScopeContext(node):


            self._definitions[-1].update(
                {k: ordered_set((v,)) for k, v in self._builtins.items()}
            )

            self._defered_annotations.append([])
            self.process_body(node.body)

            # handle function bodies
            self.process_functions_bodies()

            # handle defered annotations as in from __future__ import annotations
            self.process_annotations()
            self._defered_annotations.pop()

            # various sanity checks
            if __debug__:
                overloaded_builtins = set()
                for d in self.locals[node]:
                    name = d.name()
                    if name in self._builtins:
                        overloaded_builtins.add(name)
                    assert name in self._definitions[0], (name, d.node)

                nb_defs = len(self._definitions[0])
                nb_bltns = len(self._builtins)
                nb_overloaded_bltns = len(overloaded_builtins)
                nb_heads = len({d.name() for d in self.locals[node]})
                assert nb_defs == nb_heads + nb_bltns - nb_overloaded_bltns

        assert not self._definitions
        assert not self._defered_annotations
        assert not self._scopes
        assert not self._scope_depths
        assert not self._precomputed_locals

    def set_definition(self, name, dnode_or_dnodes, index=-1):
        if self._deadcode:
            return
        
        if isinstance(dnode_or_dnodes, Def):
            dnodes = ordered_set((dnode_or_dnodes,))
        else:
            dnodes = ordered_set(dnode_or_dnodes)

        # set the islive flag to False on killed Defs
        for d in self._definitions[index].get(name, ()):
            if not isinstance(d.node, ast.AST):
                # A builtin: we never explicitely mark the builtins as killed, since 
                # it can be easily deducted.
                continue
            if d in dnodes or any(d in definitions.get(name, ()) for 
                   definitions in self._definitions[:index]):
                # The definition exists in another definition context, so we can't
                # be sure wether it's killed or not, this happens when:
                # - a variable is conditionnaly declared (d in dnodes)
                # - a variable is conditionnaly killed (any(...))
                continue
            d.islive = False
        
        self._definitions[index][name] = dnodes

    @staticmethod
    def add_to_definition(definition, name, dnode_or_dnodes):
        if isinstance(dnode_or_dnodes, Def):
            definition[name].add(dnode_or_dnodes)
        else:
            definition[name].update(dnode_or_dnodes)

    def extend_definition(self, name, dnode_or_dnodes):
        if self._deadcode:
            return
        DefUseChains.add_to_definition(self._definitions[-1], name,
                                       dnode_or_dnodes)

    def extend_global(self, name, dnode_or_dnodes):
        if self._deadcode:
            return
        DefUseChains.add_to_definition(self._definitions[0], name,
                                       dnode_or_dnodes)

    def set_or_extend_global(self, name, dnode):
        if self._deadcode:
            return
        if name not in self._definitions[0]:
            self.locals[self.module].append(dnode)
        DefUseChains.add_to_definition(self._definitions[0], name, dnode)

    def visit_annotation(self, node):
        annotation = getattr(node, 'annotation', None)
        if annotation:
            self.visit(annotation)

    def visit_skip_annotation(self, node):
        if isinstance(node, ast.Name):
            self.visit_Name(node, skip_annotation=True)
        else:
            self.visit(node)

    def visit_FunctionDef(self, node, step=DeclarationStep):
        if step is DeclarationStep:
            dnode = self.chains.setdefault(node, Def(node))
            self.locals[self._scopes[-1]].append(dnode)

            if not self.future_annotations:
                for arg in _iter_arguments(node.args):
                    self.visit_annotation(arg)

            else:
                # annotations are to be analyzed later as well
                currentscopes = list(self._scopes)
                if node.returns:
                    self._defered_annotations[-1].append(
                        (node.returns, currentscopes, None))
                for arg in _iter_arguments(node.args):
                    if arg.annotation:
                        self._defered_annotations[-1].append(
                            (arg.annotation, currentscopes, None))

            for kw_default in filter(None, node.args.kw_defaults):
                self.visit(kw_default).add_user(dnode)
            for default in node.args.defaults:
                self.visit(default).add_user(dnode)
            for decorator in node.decorator_list:
                self.visit(decorator)

            if not self.future_annotations and node.returns:
                self.visit(node.returns)

            self.set_definition(node.name, dnode)

            self._defered.append((node,
                                  list(self._definitions),
                                  list(self._scopes),
                                  list(self._scope_depths),
                                  list(self._precomputed_locals)))
        elif step is DefinitionStep:
            with self.ScopeContext(node):
                for arg in _iter_arguments(node.args):
                    self.visit_skip_annotation(arg)
                self.process_body(node.body)
        else:
            raise NotImplementedError()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.locals[self._scopes[-1]].append(dnode)

        for base in node.bases:
            self.visit(base).add_user(dnode)
        for keyword in node.keywords:
            self.visit(keyword.value).add_user(dnode)
        for decorator in node.decorator_list:
            self.visit(decorator).add_user(dnode)

        with self.ScopeContext(node):
            self.set_definition("__class__", Def("__class__"))
            self.process_body(node.body)

        self.set_definition(node.name, dnode)


    def visit_Return(self, node):
        if node.value:
            self.visit(node.value)

    def visit_Break(self, _):
        for k, v in self._definitions[-1].items():
            DefUseChains.add_to_definition(self._breaks[-1], k, v)
        self._definitions[-1].clear()

    def visit_Continue(self, _):
        for k, v in self._definitions[-1].items():
            DefUseChains.add_to_definition(self._continues[-1], k, v)
        self._definitions[-1].clear()

    def visit_Delete(self, node):
        for target in node.targets:
            self.visit(target)

    def visit_Assign(self, node):
        # link is implicit through ctx
        self.visit(node.value)
        for target in node.targets:
            self.visit(target)

    def visit_AnnAssign(self, node):
        if node.value:
            dvalue = self.visit(node.value)
        if not self.future_annotations:
            dannotation = self.visit(node.annotation)
        else:
            self._defered_annotations[-1].append(
                (node.annotation, list(self._scopes),
                lambda d:dtarget.add_user(d)))
        dtarget = self.visit(node.target)
        if not self.future_annotations:
            dtarget.add_user(dannotation)
        if node.value:
            dvalue.add_user(dtarget)

    def visit_AugAssign(self, node):
        dvalue = self.visit(node.value)
        if isinstance(node.target, ast.Name):
            ctx, node.target.ctx = node.target.ctx, ast.Load()
            dtarget = self.visit(node.target)
            dvalue.add_user(dtarget)
            node.target.ctx = ctx
            if any(node.target.id in _globals for _globals in self._globals):
                self.extend_global(node.target.id, dtarget)
            else:
                loaded_from = [d.name() for d in self.defs(node.target,
                                                           quiet=True)]
                self.set_definition(node.target.id, dtarget)
                # If we augassign from a value that comes from '*', let's use
                # this node as the definition point.
                if '*' in loaded_from:
                    self.locals[self._scopes[-1]].append(dtarget)
        else:
            self.visit(node.target).add_user(dvalue)

    def visit_Print(self, node):
        if node.dest:
            self.visit(node.dest)
        for value in node.values:
            self.visit(value)

    def visit_For(self, node):
        self.visit(node.iter)

        self._breaks.append(defaultdict(ordered_set))
        self._continues.append(defaultdict(ordered_set))

        self._undefs.append(defaultdict(list))
        with self.DefinitionContext(self._definitions[-1].copy()) as body_defs:
            self.visit(node.target)
            self.process_body(node.body)
            self.process_undefs()

            continue_defs = self._continues.pop()
            for d, u in continue_defs.items():
                self.extend_definition(d, u)
            self._continues.append(defaultdict(ordered_set))

            # extra round to ``emulate'' looping
            self.visit(node.target)
            self.process_body(node.body)

            # process else clause in case of late break
            with self.DefinitionContext(defaultdict(ordered_set)) as orelse_defs:
                self.process_body(node.orelse)

            break_defs = self._breaks.pop()
            continue_defs = self._continues.pop()


        for d, u in orelse_defs.items():
            self.extend_definition(d, u)

        for d, u in continue_defs.items():
            self.extend_definition(d, u)

        for d, u in break_defs.items():
            self.extend_definition(d, u)

        for d, u in body_defs.items():
            self.extend_definition(d, u)

    visit_AsyncFor = visit_For

    def visit_While(self, node):

        with self.DefinitionContext(self._definitions[-1].copy()):
            self._undefs.append(defaultdict(list))
            self._breaks.append(defaultdict(ordered_set))
            self._continues.append(defaultdict(ordered_set))

            self.process_body(node.orelse)

        with self.DefinitionContext(self._definitions[-1].copy()) as body_defs:

            self.visit(node.test)
            self.process_body(node.body)

            self.process_undefs()

            continue_defs = self._continues.pop()
            for d, u in continue_defs.items():
                self.extend_definition(d, u)
            self._continues.append(defaultdict(ordered_set))

            # extra round to simulate loop
            self.visit(node.test)
            self.process_body(node.body)

            # the false branch of the eval
            self.visit(node.test)

            with self.DefinitionContext(self._definitions[-1].copy()) as orelse_defs:
                self.process_body(node.orelse)

        break_defs = self._breaks.pop()
        continue_defs = self._continues.pop()

        for d, u in continue_defs.items():
            self.extend_definition(d, u)

        for d, u in break_defs.items():
            self.extend_definition(d, u)

        for d, u in orelse_defs.items():
            self.extend_definition(d, u)

        for d, u in body_defs.items():
            self.extend_definition(d, u)

    def visit_If(self, node):
        self.visit(node.test)

        # putting a copy of current level to handle nested conditions
        with self.DefinitionContext(self._definitions[-1].copy()) as body_defs:
            self.process_body(node.body)

        with self.DefinitionContext(self._definitions[-1].copy()) as orelse_defs:
            self.process_body(node.orelse)

        for d in body_defs:
            if d in orelse_defs:
                self.set_definition(d, body_defs[d] + orelse_defs[d])
            else:
                self.extend_definition(d, body_defs[d])

        for d in orelse_defs:
            if d in body_defs:
                pass  # already done in the previous loop
            else:
                self.extend_definition(d, orelse_defs[d])

    def visit_With(self, node):
        for withitem in node.items:
            self.visit(withitem)
        self.process_body(node.body)

    visit_AsyncWith = visit_With

    def visit_Raise(self, node):
        self.generic_visit(node)

    def visit_Try(self, node):
        with self.DefinitionContext(self._definitions[-1].copy()) as failsafe_defs:
            self.process_body(node.body)
            self.process_body(node.orelse)

        # handle the fact that definitions may have fail
        for d in failsafe_defs:
            self.extend_definition(d, failsafe_defs[d])

        for excepthandler in node.handlers:
            with self.DefinitionContext(defaultdict(ordered_set)) as handler_def:
                self.visit(excepthandler)

            for hd in handler_def:
                self.extend_definition(hd, handler_def[hd])

        self.process_body(node.finalbody)

    def visit_Assert(self, node):
        self.visit(node.test)
        if node.msg:
            self.visit(node.msg)

    def visit_Import(self, node):
        for alias in node.names:
            dalias = self.chains.setdefault(alias, Def(alias))
            base = alias.name.split(".", 1)[0]
            self.set_definition(alias.asname or base, dalias)
            self.locals[self._scopes[-1]].append(dalias)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            dalias = self.chains.setdefault(alias, Def(alias))
            if alias.name == '*':
                self.extend_definition('*', dalias)
            else:
                self.set_definition(alias.asname or alias.name, dalias)
            self.locals[self._scopes[-1]].append(dalias)

    def visit_Exec(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.body)

        if node.globals:
            self.visit(node.globals)
        else:
            # any global may be used by this exec!
            for defs in self._definitions[0].values():
                for d in defs:
                    d.add_user(dnode)

        if node.locals:
            self.visit(node.locals)
        else:
            # any local may be used by this exec!
            visible_locals = set()
            for _definitions in reversed(self._definitions[1:]):
                for dname, defs in _definitions.items():
                    if dname not in visible_locals:
                        visible_locals.add(dname)
                        for d in defs:
                            d.add_user(dnode)

        self.extend_definition("*", dnode)

    def visit_Global(self, node):
        for name in node.names:
            self._globals[-1].add(name)

    def visit_Nonlocal(self, node):
        for name in node.names:
            for d in reversed(self._definitions[:-1]):
                if name not in d:
                    continue
                else:
                    # this rightfully creates aliasing
                    self.set_definition(name, d[name])
                    break
            else:
                self.unbound_identifier(name, node)

    def visit_Expr(self, node):
        self.generic_visit(node)

    # expr
    def visit_BoolOp(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        for value in node.values:
            self.visit(value).add_user(dnode)
        return dnode

    def visit_BinOp(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.left).add_user(dnode)
        self.visit(node.right).add_user(dnode)
        return dnode

    def visit_UnaryOp(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.operand).add_user(dnode)
        return dnode

    def visit_Lambda(self, node, step=DeclarationStep):
        if step is DeclarationStep:
            dnode = self.chains.setdefault(node, Def(node))
            for default in node.args.defaults:
                self.visit(default).add_user(dnode)
            self._defered.append((node,
                                  list(self._definitions),
                                  list(self._scopes),
                                  list(self._scope_depths),
                                  list(self._precomputed_locals)))
            return dnode
        elif step is DefinitionStep:
            dnode = self.chains[node]
            with self.ScopeContext(node):
                for a in node.args.args:
                    self.visit(a)
                self.visit(node.body).add_user(dnode)
            return dnode
        else:
            raise NotImplementedError()

    def visit_IfExp(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.test).add_user(dnode)
        self.visit(node.body).add_user(dnode)
        self.visit(node.orelse).add_user(dnode)
        return dnode

    def visit_Dict(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        for key in filter(None, node.keys):
            self.visit(key).add_user(dnode)
        for value in node.values:
            self.visit(value).add_user(dnode)
        return dnode

    def visit_Set(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        for elt in node.elts:
            self.visit(elt).add_user(dnode)
        return dnode

    def visit_ListComp(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        try:
            _validate_comprehension(node)
        except SyntaxError as e:
            self.warn(str(e), node)
            return dnode
        with self.CompScopeContext(node):
            for i, comprehension in enumerate(node.generators):
                self.visit_comprehension(comprehension, 
                                         is_nested=i!=0).add_user(dnode)
            self.visit(node.elt).add_user(dnode)

        return dnode

    visit_SetComp = visit_ListComp

    def visit_DictComp(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        try:
            _validate_comprehension(node)
        except SyntaxError as e:
            self.warn(str(e), node)
            return dnode
        with self.CompScopeContext(node):
            for i, comprehension in enumerate(node.generators):
                self.visit_comprehension(comprehension, 
                                         is_nested=i!=0).add_user(dnode)
            self.visit(node.key).add_user(dnode)
            self.visit(node.value).add_user(dnode)

        return dnode

    visit_GeneratorExp = visit_ListComp

    def visit_Await(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.value).add_user(dnode)
        return dnode

    def visit_Yield(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        if node.value:
            self.visit(node.value).add_user(dnode)
        return dnode

    visit_YieldFrom = visit_Await

    def visit_Compare(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.left).add_user(dnode)
        for expr in node.comparators:
            self.visit(expr).add_user(dnode)
        return dnode

    def visit_Call(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.func).add_user(dnode)
        for arg in node.args:
            self.visit(arg).add_user(dnode)
        for kw in node.keywords:
            self.visit(kw.value).add_user(dnode)
        return dnode

    visit_Repr = visit_Await

    def visit_Constant(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        return dnode

    def visit_FormattedValue(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.value).add_user(dnode)
        if node.format_spec:
            self.visit(node.format_spec).add_user(dnode)
        return dnode

    def visit_JoinedStr(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        for value in node.values:
            self.visit(value).add_user(dnode)
        return dnode

    visit_Attribute = visit_Await

    def visit_Subscript(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.value).add_user(dnode)
        self.visit(node.slice).add_user(dnode)
        return dnode

    def visit_Starred(self, node):
        if isinstance(node.ctx, ast.Store):
            return self.visit(node.value)
        else:
            dnode = self.chains.setdefault(node, Def(node))
            self.visit(node.value).add_user(dnode)
            return dnode

    def visit_NamedExpr(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.value).add_user(dnode)
        if isinstance(node.target, ast.Name):
            self.visit_Name(node.target, named_expr=True)
        return dnode

    def is_in_current_scope(self, name):
        return any(name in defs
                   for defs in self._definitions[self._scope_depths[-1]:])

    def _first_non_comprehension_scope(self):
        index = -1
        enclosing_scope = self._scopes[index]
        while isinstance(enclosing_scope, (ast.DictComp, ast.ListComp, 
                                            ast.SetComp, ast.GeneratorExp)):
            index -= 1
            enclosing_scope = self._scopes[index]
        return index, enclosing_scope

    def visit_Name(self, node, skip_annotation=False, named_expr=False):
        if isinstance(node.ctx, (ast.Param, ast.Store)):
            dnode = self.chains.setdefault(node, Def(node))
            if any(node.id in _globals for _globals in self._globals):
                self.set_or_extend_global(node.id, dnode)
            else:
                # special code for warlus target: should be 
                # stored in first non comprehension scope
                index, enclosing_scope = (self._first_non_comprehension_scope() 
                                          if named_expr else (-1, self._scopes[-1]))

                if index < -1 and isinstance(enclosing_scope, ast.ClassDef):
                    # invalid named expression, not calling set_definition.
                    self.warn('assignment expression within a comprehension '
                              'cannot be used in a class body', node)
                    return dnode
            
                self.set_definition(node.id, dnode, index)
                if dnode not in self.locals[self._scopes[index]]:
                    self.locals[self._scopes[index]].append(dnode)

            # Name.annotation is a special case because of gast
            if node.annotation is not None and not skip_annotation and not self.future_annotations:
                self.visit(node.annotation)


        elif isinstance(node.ctx, (ast.Load, ast.Del)):
            node_in_chains = node in self.chains
            if node_in_chains:
                dnode = self.chains[node]
            else:
                dnode = Def(node)
            for d in self.defs(node):
                d.add_user(dnode)
            if not node_in_chains:
                self.chains[node] = dnode
            # currently ignore the effect of a del
        else:
            raise NotImplementedError()
        return dnode

    def visit_Destructured(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        tmp_store = ast.Store()
        for elt in node.elts:
            if isinstance(elt, ast.Name):
                tmp_store, elt.ctx = elt.ctx, tmp_store
                self.visit(elt)
                tmp_store, elt.ctx = elt.ctx, tmp_store
            elif isinstance(elt, (ast.Subscript, ast.Starred, ast.Attribute)):
                self.visit(elt)
            elif isinstance(elt, (ast.List, ast.Tuple)):
                self.visit_Destructured(elt)
        return dnode

    def visit_List(self, node):
        if isinstance(node.ctx, ast.Load):
            dnode = self.chains.setdefault(node, Def(node))
            for elt in node.elts:
                self.visit(elt).add_user(dnode)
            return dnode
        # unfortunately, destructured node are marked as Load,
        # only the parent List/Tuple is marked as Store
        elif isinstance(node.ctx, ast.Store):
            return self.visit_Destructured(node)

    visit_Tuple = visit_List

    # slice

    def visit_Slice(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        if node.lower:
            self.visit(node.lower).add_user(dnode)
        if node.upper:
            self.visit(node.upper).add_user(dnode)
        if node.step:
            self.visit(node.step).add_user(dnode)
        return dnode

    # misc

    def visit_comprehension(self, node, is_nested):
        dnode = self.chains.setdefault(node, Def(node))
        if not is_nested and sys.version_info.major >= 3:
            # There's one part of a comprehension or generator expression that executes in the surrounding scope, 
            # it's the expression for the outermost iterable.
            with self.SwitchScopeContext(self._definitions[:-1], self._scopes[:-1], 
                                        self._scope_depths[:-1], self._precomputed_locals[:-1]):
                self.visit(node.iter).add_user(dnode)
        else:
            # If a comprehension has multiple for clauses, 
            # the iterables of the inner for clauses are evaluated in the comprehension's scope:
            self.visit(node.iter).add_user(dnode)
        self.visit(node.target)
        for if_ in node.ifs:
            self.visit(if_).add_user(dnode)
        return dnode

    def visit_excepthandler(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        if node.type:
            self.visit(node.type).add_user(dnode)
        if node.name:
            self.visit(node.name).add_user(dnode)
        self.process_body(node.body)
        return dnode

    def visit_arguments(self, node):
        for arg in _iter_arguments(node):
            self.visit(arg)

    def visit_withitem(self, node):
        dnode = self.chains.setdefault(node, Def(node))
        self.visit(node.context_expr).add_user(dnode)
        if node.optional_vars:
            self.visit(node.optional_vars)
        return dnode