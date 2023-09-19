"""
This is the module from duc construction, which is forked from [beniget project](https://github.com/serge-sans-paille/beniget/blob/master/beniget/beniget.py).
"""
import sys, builtins
from typing import List, Dict, Union, Set, Tuple, Callable, Optional, Any
from collections import defaultdict
from contextlib import contextmanager
from .exceptions import _StopTraversal
from .ordered_set import ordered_set
import gast as ast 



Builtins = dict(builtins.__dict__.items())
Builtins["__file__"] = __file__
DeclarationStep = object()
DefinitionStep =  object()

class Def:
    """
    Model a definition, either named or unnamed, and its users.
    """
    def __init__(self, node):
        self.node = node
        self._users = ordered_set()
        self.islive = True

    def add_user(self, node):
        assert isinstance(node, Def)
        self._users.add(node)

    def name(self)->str:
        if type(self.node) in (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef):
            return self.node.name
        elif type(self.node) ==  ast.Name:
            return self.node.id
        elif type(self.node) ==  ast.alias:
            base = self.node.name.split(".", 1)[0]
            return self.node.asname or base
        elif type(self.node) == tuple:
            return self.node[1]
        else: # Return its type otherwise. 
            return type(self.node).__name__

    def users(self)->List:
        return self._users

    def __repr__(self)->str:
        return self._repr({})

    def _repr(self, nodes)->str:
        if self in nodes:
            return f"(#{nodes[self]})"
        nodes[self] = len(nodes)
        return f'{self.node} -> ({", ".join(u._repr(nodes.copy()) for u in self._users)})'

    def __str__(self):
        return self._str({})

    def _str(self, nodes):
        if self in nodes:
            return f"(#{nodes[self]})"
        nodes[self] = len(nodes)
        return f'{self.name()} -> ({", ".join(u._str(nodes.copy()) for u in self._users)})'


class _CollectFutureImports(ast.NodeVisitor):
    """
    A future statement must appear near the top of the module. So the only lines before a future statement are:
     1. the module docstring (if any),
     2. comments,
     3. blank lines, and
     4. other future statements.
    As long as something else is visited, we can stop the visit.
    """
    def __init__(self):
        self.FutureImports:set[str] = set() 

    def visit_Module(self, node):
        for child in node.body:
            try:
                self.visit(child)
            except _StopTraversal:
                break

    def visit_ImportFrom(self, node):
        if node.level or node.module != '__future__':
            raise _StopTraversal()
        self.FutureImports.update((al.name for al in node.names))

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_Constant(self, node):
        if not isinstance(node.value, str):
            raise _StopTraversal()

    def generic_visit(self, node):
        raise _StopTraversal()

class CollectLocals(ast.NodeVisitor):
    def __init__(self):
        self.Locals = set()
        self.NonLocals = set()

    def visit_FunctionDef(self, node):
        # no recursion
        self.Locals.add(node.name)
    def visit_Nonlocal(self, node):
        self.NonLocals.update(iter(node.names))
    # some trivial cases
    visit_AsyncFunctionDef = visit_FunctionDef
    visit_ClassDef = visit_FunctionDef
    visit_Global = visit_Nonlocal

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store) and node.id not in self.NonLocals:
            self.Locals.add(node.id)

    def visit_Import(self, node):
        for alias in node.names:
            base = alias.name.split(".", 1)[0]
            self.Locals.add(alias.asname or base)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.Locals.add(alias.asname or alias.name)
    def skip(self, _):
        pass
    visit_SetComp = visit_DictComp = visit_ListComp = skip
    visit_GeneratorExp  = visit_Lambda = skip # skip generators

def collect_locals(node)->set:
    '''
    Compute the set of identifiers local to a given node by emulating a call to locals()
    '''
    visitor = CollectLocals()
    visitor.generic_visit(node)
    return visitor.Locals


class DefUseChains(ast.NodeVisitor):
    def __init__(self, filename=None):
        """
        - locals: Dict[node, List[Def]], a mapping between a node and the list of variable defined in this node,
        - chains: Dict[node, Def], a mapping between nodes and their chains.
        """
        self.chains:Dict[node, Def]= {}
        self.locals:Dict[node, List[Def]] = defaultdict(list)

        self.filename = filename if filename is not None else "<unknown>"
        # deep copy of builtins, to remain reentrant
        self._builtins = {k: Def(v) for k, v in Builtins.items()}

        # function body are not executed when the function definition is met
        # this holds a list of the functions met during body processing
        self._defered = []
       
        self._definitions = []  # stack of mapping between an id and Names
        self._scope_depths = []  # stack of scope depth
        self._globals = []   # stack of variable defined with the global keywords
       
        self._precomputed_locals = []  # stack of local identifiers, used to detect 'read before assign'

        self._undefs = [] # stack of variable that were undefined when we met them, but that may be defined in another path of the control flow
        self._scopes = [] # stack of nodes starting a scope: class, module, function, generator expression, comprehension...

        self._breaks = []
        self._continues = []

        '''
        stack of list of annotations (annotation, heads, callback),
        # only used in the case of from __future__ import annotations feature.
        # the annotations are analyzed when the whole module has been processed,
        # it should be compatible with PEP 563, and minor changes are required to support PEP 649.
        '''
        self._defered_annotations = []

        # dead code levels, it's non null for code that cannot be executed
        self._deadcode = 0

        # attributes set in visit_Module
        self.module = None
        self.future_annotations = False
        
    
    ## helpers
    def _dump_locals(self, node, only_live=False):
        """
        Like `dump_definitions` but returns the result grouped by symbol name and it includes linenos.
        :Returns: List of string formatted like: '{symbol name}:{def lines}'
        """
        groupped = defaultdict(list)
        for d in self.locals[node]:
            if not only_live or d.islive:
                groupped[d.name()].append(d)
        return [
            f"{name}:{','.join([str(getattr(d.node, 'lineno', -1)) for d in defs])}"
            for name, defs in groupped.items()
        ]

    def dump_definitions(self, node, ignore_builtins=True):
        if not isinstance(node, ast.Module) or ignore_builtins:
            return sorted(d.name() for d in self.locals[node])
        builtins = set(self._builtins.values())
        return sorted(d.name() for d in self.locals[node] if d not in builtins)

    def dump_chains(self, node):
        return [str(d) for d in self.locals[node]]

    def location(self, node):
        if hasattr(node, "lineno"):
            filename = f'{"<unknown>" if self.filename is None else self.filename}:'
            return f" at {filename}{node.lineno}:{node.col_offset}"
        return ""

    def unbound_identifier(self, name, node):
        self.warn(f"unbound identifier '{name}'", node)
    
    def warn(self, msg, node):
        ## TODO: add a logger
        print(f"W: {msg}{self.location(node)}")

    def invalid_name_lookup(self, name, scope, precomputed_locals, local_defs):
        # We may hit the situation where we refer to a local variable which is
        # not bound yet. This is a runtime error in Python, so we try to detect it statically.
        # not a local variable => fine
        if name not in precomputed_locals:
            return

        # It's meant to be a local variable, but it's not defined yet.
        is_local = any((name in defs or '*' in defs) for defs in local_defs)

        # At class scope, it's ok to refer to a global even if we also have a
        # local definition for that variable. Stated other wise
        #
        # >>> a = 1
        # >>> def foo(): a = a
        # >>> foo() # fails, a is a local referenced before being assigned
        # >>> class bar: a = a
        # >>> bar() # ok, and `bar.a is a`
        if isinstance(scope, ast.ClassDef):
            top_level_definitions = self._definitions[:-self._scope_depths[0]]
            tmp_is_global = [(name in top_lvl_def or '*' in top_lvl_def) for top_lvl_def in top_level_definitions]
            is_global = any(tmp_is_global)
            return  not (is_local or is_global) # not local, not global 
        
        return not is_local

    def compute_annotation_defs(self, node, quiet=False):
        name = node.id
        try:
             # resolving an annotations is different.
            return lookup_annotation_name_defs(name, self._scopes, self.locals)
        except LookupError:
            # fallback to regular behaviour on module scope
            # to support names from builtins or wildcard imports.
            return self.compute_defs(node, quiet=quiet)

    def compute_defs(self, node, quiet=False):
        '''
        Performs an actual lookup of node's id in current context, returning the list of def linked to that use.
        '''
        name = node.id
        stars = []

        # If the `global` keyword has been used, honor it
        if any(name in _globals for _globals in self._globals):
            looked_up_definitions = self._definitions[:-self._scope_depths[0]]
        else:
            looked_up_definitions = self._extracted_from_compute_defs_15(name)
        for defs in looked_up_definitions:
            if defs is StopIteration:
                break
            elif name in defs:
                return stars + list(defs[name]) if stars else defs[name]
            elif "*" in defs:
                stars.extend(defs["*"])

        d = self.chains.setdefault(node, Def(node))

        if self._undefs:
            self._undefs[-1][name].append((d, stars))

        if stars:
            return stars + [d]
        if not self._undefs and not quiet:
            self.unbound_identifier(name, node)
        return [d]

    # TODO Rename this here and in `compute_defs`
    def _extracted_from_compute_defs_15(self, name):
            # List of definitions to check. This includes all non-class definitions *and* the last definition. Class definitions are not
            # included because they require fully qualified access.
        result = []

        scopes_iter = iter(reversed(self._scopes))
        depths_iter = iter(reversed(self._scope_depths))
        precomputed_locals_iter = iter(reversed(self._precomputed_locals))

        # Keep the last scope because we could be in class scope, so no need need for fully qualified access.
        lvl = depth = next(depths_iter)
        precomputed_locals = next(precomputed_locals_iter)
        base_scope = next(scopes_iter)
        defs = self._definitions[depth:]
        if not self.invalid_name_lookup(name, base_scope, precomputed_locals, defs):
            result.extend(reversed(defs))
                # Iterate over scopes, filtering out class scopes.
            for scope, depth, precomputed_locals in zip(scopes_iter, depths_iter, precomputed_locals_iter):
                if not isinstance(scope, ast.ClassDef):
                    defs = self._definitions[lvl + depth: lvl]
                    if self.invalid_name_lookup(name, base_scope, precomputed_locals, defs):
                        result.append(StopIteration)
                        break
                    result.extend(reversed(defs))
                lvl += depth

        return result

    defs = compute_defs

    def process_body(self, stmts):
        deadcode = False
        for stmt in stmts:
            self.visit(stmt)
            if isinstance(stmt, (ast.Break, ast.Continue, ast.Raise)) and not deadcode:
                deadcode = True
                self._deadcode += 1
        if deadcode:
            self._deadcode -= 1
            
    def process_undefs(self):
        if not self._undefs:
            return
        # Retrieve the latest (or last) sets of undefined variables and definitions
        last_undefs = self._undefs[-1]
        last_definitions = self._definitions[-1] if self._definitions else {}
        # Iterate through each undefined variable/reference
        for undef_name, undef_entries in last_undefs.items():
            # If the undefined variable has a definition in the latest definitions
            if undef_name in last_definitions:                
                # For each new definition of the undefined variable,   
                # Accumulate all users of the undefined variable and add each user to the new definition
                for new_definition in last_definitions[undef_name]:
                    users_to_add = [user for undef, _ in undef_entries for user in undef.users()]
                    for user in users_to_add:
                        new_definition.add_user(user)
            else:
                # If the variable is undefined and has no definition, If 'stars' flag is False, raise an "unbound identifier" exception
                for undef, stars in undef_entries:
                    if not stars:
                        self.unbound_identifier(undef_name, undef.node)

        # Remove the last processed set of undefined variables/references
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

    CompScopeContext = ScopeContext # comphresion container is a scope, same as a function.
    
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
            visitor = getattr(self, f"visit_{type(fnode).__name__}")
            with self.SwitchScopeContext(defs, scopes, scope_depths, precomputed_locals):
                visitor(fnode, step=DefinitionStep)

    def process_annotations(self):
        compute_defs, self.defs = self.defs,  self.compute_annotation_defs
        for annnode, heads, cb in self._defered_annotations[-1]:
            visitor = getattr(self, f"visit_{type(annnode).__name__}")
            currenthead, self._scopes = self._scopes, heads
            cb(visitor(annnode)) if cb else visitor(annnode)
            self._scopes = currenthead
        self.defs = compute_defs

    # Some functions to hanle each constructs in ASTs 
    def visit_Module(self, node):
        self.module = node 
        cf = _CollectFutureImports()
        cf.visit(node)
        futures =  cf.FutureImports
        # determine whether the PEP563 is enabled
        # allow manual enabling of DefUseChains.future_annotations
        self.future_annotations |= 'annotations' in futures

        with self.ScopeContext(node):
            self._extracted_from_visit_Module_11(node)
        assert not self._definitions
        assert not self._defered_annotations
        assert not self._scopes
        assert not self._scope_depths
        assert not self._precomputed_locals

    # TODO Rename this here and in `visit_Module`
    def _extracted_from_visit_Module_11(self, node):
        self._definitions[-1].update( {k: ordered_set((v,)) for k, v in self._builtins.items()})
        self._defered_annotations.append([])
        self.process_body(node.body)

        # handle function bodies
        self.process_functions_bodies()

        # handle defered annotations as in from __future__ import annotations
        self.process_annotations()
        self._defered_annotations.pop()

            # various sanity checks
        if __debug__:
            self._extracted_from_visit_Module_24(node)

    # TODO Rename this here and in `visit_Module`
    def _extracted_from_visit_Module_24(self, node):
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
    def add_to_definition(definition, name, dnode_or_dnodes:Union[Def, List[Def]]):
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
        if annotation := getattr(node, 'annotation', None):
            self.visit(annotation)

    def visit_skip_annotation(self, node):
        if isinstance(node, ast.Name):
            self.visit_Name(node, skip_annotation=True)
        else:
            self.visit(node)

    def visit_FunctionDef(self, node, step=DeclarationStep):
        if step is DeclarationStep:
            self._extracted_from_visit_FunctionDef_3(node)
        elif step is DefinitionStep:
            with self.ScopeContext(node):
                for arg in _iter_arguments(node.args):
                    self.visit_skip_annotation(arg)
                self.process_body(node.body)
        else:
            raise NotImplementedError()

    # TODO Rename this here and in `visit_FunctionDef`
    def _extracted_from_visit_FunctionDef_3(self, node):
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
                # If we augassign from a value that comes from '*', let's use this node as the definition point.
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
            if d not in body_defs:
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
        return self.chains.setdefault(node, Def(node))
       
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
            dnode = self.chains[node] if node_in_chains else Def(node)
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
        if not is_nested:
            # There's one part of a comprehension or generator expression that executes in the surrounding scope, it's the expression for the outermost iterable.
            with self.SwitchScopeContext(self._definitions[:-1], self._scopes[:-1], 
                                        self._scope_depths[:-1], self._precomputed_locals[:-1]):
                self.visit(node.iter).add_user(dnode)
        else:
            # If a comprehension has multiple for clauses, the iterables of the inner for clauses are evaluated in the comprehension's scope:
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


def _validate_comprehension(node):
    """
    Raises SyntaxError if:
     1. a named expression is used in a comprehension iterable expression
     2. a named expression rebinds a comprehension iteration variable
    """
    iter_names = set() # comprehension iteration variables
    find_iter_names = lambda n: (n.id for n in ast.walk(n) if isinstance(n, ast.NamedExpr))
    for gen in node.generators:
        for _ in (n for n in ast.walk(gen.iter) if isinstance(n, ast.NamedExpr)):
            raise SyntaxError('assignment expression cannot be used ''in a comprehension iterable expression')
        iter_names.update(n.id for n in ast.walk(gen.target) 
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store))
    for namedexpr in (n for n in ast.walk(node) if  isinstance(n, ast.NamedExpr)):
        bound = getattr(namedexpr.target, 'id', None)
        if bound in iter_names:
            raise SyntaxError(
                f"assignment expression cannot rebind comprehension iteration variable '{bound}'"
            )

def _iter_arguments(args):
    """
    Yields all arguments of the given ast.arguments instance.
    """
    yield from args.args
    yield from args.posonlyargs
    if args.vararg:
        yield args.vararg
    yield from args.kwonlyargs
    if args.kwarg:
        yield args.kwarg

def lookup_annotation_name_defs(name, heads, locals_map):
    r"""
    Simple identifier -> defs resolving.

    Lookup a name with the provided head nodes using the locals_map.
    Note that nonlocal and global keywords are ignored by this function.
    Only used to resolve annotations when PEP 563 is enabled.

    :param name: The identifier we're looking up.
    :param heads: List of ast scope statement that describe
        the path to the name context. i.e ``[<Module>, <ClassDef>, <FunctionDef>]``.
        The lookup will happend in the context of the body of tail of ``heads``
        Can be gathered with `Ancestors.parents`.
    :param locals_map: `DefUseChains.locals`.

    :raise LookupError: For
        - builtin names
        - wildcard imported names
        - unbound names

    :raise ValueError: When the heads is empty.
    This function can be used by client code like this:
    """
    scopes = _get_lookup_scopes(heads)
    scopes_len = len(scopes)
    if scopes_len>1:
        # start by looking at module scope first, then try the theoretical runtime scopes.
        # putting the global scope last in the list so annotation are esolve using he global namespace first. this is the way pyright does.
        scopes.append(scopes.pop(0))
    try:
        return _lookup(name, scopes, locals_map)
    except LookupError as e:
        raise LookupError(
            f"'{name}' not found in {heads[-1]}, might be a builtin"
        ) from e

def _get_lookup_scopes(heads):
    '''
    heads[-1] is the direct enclosing scope and heads[0] is the module.
    returns a list based on the elements of heads, but with
    the ignorable scopes removed. Ignorable in the sens that the lookup
    will never happend in this scope for the given context.
    More of less modeling in [Guido van Rossum's blog post](https://github.com/gvanrossum/gvanrossum.github.io/blob/main/formal/scopesblog.md)
    '''
    heads = list(heads) # avoid modifying the list (important)
    try:
        direct_scope = heads.pop(-1) # this scope is the only one that can be a class
    except IndexError as e:
        raise ValueError('invalid heads: must include at least one element') from e
    try:
        global_scope = heads.pop(0)
    except IndexError:
        # we got only a global scope
        return [direct_scope]
    other_scope_type = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.DictComp, ast.ListComp, ast.SetComp, ast.GeneratorExp)
    other_scopes = list(filter(lambda s:type(s) in other_scope_type, heads))# [s for s in heads if isinstance(s, other_scope_type)]
    return [global_scope] + other_scopes + [direct_scope]

def _lookup(name, scopes, locals_map):
    context = scopes.pop()
    if defs := [
        loc
        for loc in locals_map.get(context, ())
        if loc.name() == name and loc.islive
    ]:
        return defs
    elif len(scopes)==0:
        raise LookupError()
    return _lookup(name, scopes, locals_map)

class UseDefChains(object):
    """
    DefUseChains adaptor that builds a mapping between each user
    and the Def that defines this user:
        - chains: Dict[node, List[Def]], a mapping between nodes and the Defs
          that define it.
    """

    def __init__(self, defuses):
        self.chains = {}
        for chain in defuses.chains.values():
            if isinstance(chain.node, ast.Name):
                self.chains.setdefault(chain.node, [])
            for use in chain.users():
                self.chains.setdefault(use.node, []).append(chain)

        for chain in defuses._builtins.values():
            for use in chain.users():
                self.chains.setdefault(use.node, []).append(chain)

    def __str__(self):
        out = []
        for k, uses in self.chains.items():
            kname = Def(k).name()
            kstr = "{} <- {{{}}}".format(
                kname, ", ".join(sorted(use.name() for use in uses))
            )
            out.append((kname, kstr))
        out.sort()
        return ", ".join(s for k, s in out)
