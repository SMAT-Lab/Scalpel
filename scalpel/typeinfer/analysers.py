"""
This module contains a set of helper classes for type inference, e.g. a few ast visitors for extracting data, heuristic
functions, etc.
"""

import ast
import re
import tokenize
from typed_ast import ast3
import typeshed_client
from typing import List, Dict

from scalpel.cfg import CFGBuilder
from scalpel.typeinfer.classes import BinaryOperation, ScalpelVariable, ScalpelFunction, ScalpelClass
from scalpel.typeinfer.visitors import get_func_calls_type as get_func_calls, get_call_type
from scalpel.typeinfer.utilities import (
    get_type,
    get_attr_name,
    get_built_in_types,
    resolve_name,
    check_consistent_list_types
)

from scalpel.SSA.const import SSA


class BinaryOperatorMap:
    """
    Class for storing binary operation information
    """

    def __init__(self):
        self.hash: Dict[str, list] = {}
        self._type_hash: Dict[str, any] = {}

    def append(self, operation: BinaryOperation):
        # Left variable
        if self.hash.get(operation.left):
            self.hash[operation.left].append(operation)
        else:
            self.hash[operation.left] = [operation]

        # Right variable
        if self.hash.get(operation.right):
            self.hash[operation.right].append(operation)
        else:
            self.hash[operation.right] = [operation]

        # Variable hashing
        self._type_hash[operation.left] = operation.left_ast_type
        self._type_hash[operation.right] = operation.right_ast_type

    def __getitem__(self, item):
        hashed = self.hash.get(item)
        if hashed:
            return hashed
        return None

    def chain_types(self):

        #TODO: Chain together types of variables involved in binary operations to determine types
        for variable, operation_list in self.hash.items():
            if isinstance(self._type_hash.get(variable), ast.Constant):
                pass


class _StaticAnalyzer(ast.NodeVisitor):
    """
    The base class of analyzer, provides functions that read and parse a python program file
    """
    def __init__(self):
        self.file_name = None

    def check(self, paths):
        for filepath in paths:
            self.file_name = filepath
            tree = ast.parse(_StaticAnalyzer.read_file(self.file_name))
            self.visit(tree)

    @staticmethod
    def read_file(file_name: str):
        """
        Read a file as tokens

        Args:
            file_name: The name of the file to read
        Returns:
            The read file tokens
        """
        with tokenize.open(file_name) as file:
            return file.read()


class ImportTypeMap(_StaticAnalyzer):
    """
    Class for mapping imported functions, variables, etc. to their types
    """

    def __init__(self, root):
        """
        Args:
            root: The root node of the input source file.
        """
        super().__init__()
        self.imports: Dict[str, str] = {}
        self.typeshed_resolver = typeshed_client.Resolver()
        self.root = root

    def map(self):
        """
        Get the import type map
        """
        import_mappings = {}  # Maps imported functions, variables, etc. to their types
        imports = {}  # Keeps a dictionary of imported libraries
        module = None
        for node in ast.iter_child_nodes(self.root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    module = node.module.split('.')
            else:
                continue

            for names in node.names:
                if module:
                    for name in names.name.split('.'):
                        import_name = ".".join(module + [name])
                        if module:
                            # Importing from module
                            import_type = self.get_imported_type(import_name)
                            if import_type is not None:
                                import_mappings[name] = import_type
                        else:
                            # Importing whole module
                            imports[import_name] = True

        return import_mappings, imports

    def get_imported_type(self, import_name: str):
        """
        Get the type of an imported function, variable, etc.
        Args:
            import_name: a fully qualified name of the function, the variable, etc.

        """
        fully_qualified_name = self.typeshed_resolver.get_fully_qualified_name(import_name)
        if isinstance(fully_qualified_name, typeshed_client.parser.NameInfo):
            node = fully_qualified_name.ast
            if isinstance(node, ast.FunctionDef):
                if isinstance(node.returns, ast3.Subscript):
                    return node.returns.value.id

                if isinstance(node.returns, ast.Name):
                    return node.returns.id
            elif isinstance(node, ast3.AnnAssign):
                if hasattr(node.annotation, "id"):
                    return node.annotation.id
                # bad catchall, will throw exception but we can improve on in future
                else:
                    return node.annotation.value.id
            elif isinstance(node, ast3.ClassDef):
                return node.name  # Type is class name
        return None


class ClassDefinitionMap(_StaticAnalyzer):
    """
    Class for retrieving class definitions in a file
    """

    def __init__(self, root):
        """
        Args:
            root: The root node of the input source file.
        """
        super().__init__()
        self.root = root

    def map(self) -> List[ScalpelClass]:
        """
        Get the class definitions
        """
        class_definitions = []
        for node in ast.iter_child_nodes(self.root):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                inheritance = [n.id for n in node.bases]
                methods = []
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        # We don't pass return type into function def since we will figure it out later
                        methods.append(ScalpelFunction(
                            name=n.name,
                            line=n.lineno
                        ))
                class_definitions.append(ScalpelClass(
                    name=class_name,
                    methods=methods,
                    inherits=inheritance
                ))

        return class_definitions


class FunctionDefinitionMap(_StaticAnalyzer):
    """
    Class for retrieving functions definitions in a file
    """

    def __init__(self, root):
        """
        Args:
            root: The root node of the input source file.
        """
        super().__init__()
        self.root = root

    def map(self) -> List[ScalpelFunction]:
        """
        Get the function definitions
        """
        function_definitions = []
        for node in ast.iter_child_nodes(self.root):
            if isinstance(node, ast.FunctionDef):
                # We don't pass return type into function def since we will figure it out later
                # Also worth noting that this won't pick up on methods defined in classes
                function_definitions.append(ScalpelFunction(
                    name=node.name,
                    line=node.lineno
                ))

        return function_definitions


class VariableAssignmentMap(_StaticAnalyzer):
    """
    Class for retrieving variable assignments
    """

    def __init__(self, root, imports=None):
        """
        Args:
            root: The root node of the input source file.
            imports: The import type map of the input source file
        """
        super().__init__()
        if imports is None:
            imports = {}
        self.root = root
        self.imports = imports  # Pass in the imported types for a files

    def map(self) -> List[ScalpelVariable]:
        """
        Get the variable assignments
        """
        # TODO: Ensure coverage of all variable types
        # TODO: Double variable assignment, e.g. if True: x = 5; else: x = "Hello";
        variables = []
        for node in ast.walk(self.root):
            if isinstance(node, ast.FunctionDef):
                # Function arguments
                for arg in node.args.args:
                    if arg.arg != 'self':
                        variable = ScalpelVariable(
                            name=arg.arg,
                            function=node.name,
                            line=node.lineno,
                            type=any.__name__,
                            is_arg=True
                        )
                        variables.append(variable)
            elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                variable_names = []
                variable_name = node.targets[0].id
                assignment_type = any.__name__

                variable = ScalpelVariable(
                    name=variable_name,
                    function="",
                    line=node.lineno,
                    type=assignment_type
                )
                variable_type = 'any'
                if isinstance(node.value, ast.Call) and not isinstance(node.value.func, ast.Attribute):

                    # Assignment is to a callable
                    if isinstance(node.value.func, ast.Name):
                        called = node.value.func.id  # Name of callable
                        # Check to see if it is an imported callable
                        imported_type = self.imports.get(called)
                        if imported_type:
                            variable_type = imported_type

                elif isinstance(node.value, ast.Constant):
                    # String, int, float, boolean
                    variable_type = type(node.value.value).__name__  # Determine specific type
                elif isinstance(node.value, ast.Dict):
                    # Dictionary
                    key_type = check_consistent_list_types(node.value.keys)
                    value_type = check_consistent_list_types(node.value.values)
                    variable_type = f"Dict[{key_type}, {value_type}]"
                elif isinstance(node.value, ast.List) or isinstance(node.value, ast.Tuple):
                    # List or tuple, check to see if types in list are constant
                    values = node.value.elts
                    value_type = check_consistent_list_types(values)
                    variable_type = f"{type(node.value).__name__}[{value_type}]"
                elif isinstance(node.value, ast.ListComp):
                    variable_type = list.__name__
                elif isinstance(node.value, ast.IfExp) or isinstance(node.value, ast.Compare):
                    # Boolean, see heuristic 4
                    variable_type = bool.__name__
                elif isinstance(node.value, ast.BinOp):
                    # Assignment to result of binary operation
                    variable.binary_operation = node.value
                elif isinstance(node.value, ast.BoolOp):
                    variable_type = bool.__name__

                variable.type = variable_type
                if variable_name not in variable_names:
                    variable_names.append(variable_name)
                    variables.append(variable)
                else:
                    # Multiple declarations of the same variable
                    # TODO: Add union types here?
                    pass
        return variables


class BinaryOperationMap(_StaticAnalyzer):
    """
    Class for retrieving binary operations
    """

    def __init__(self, root):
        """
        Args:
            root: The root node of the input source file.
        """
        super().__init__()
        self.root = root

    def map(self) -> BinaryOperatorMap:
        """
        Get the binary operations
        """

        binary_operator_map = BinaryOperatorMap()
        for node in ast.walk(self.root):

            if isinstance(node, ast.BinOp):
                # Check to see if we have an easily resolvable variable type since this will allow
                # us to determine the type of all variables involved in the binary operation
                if isinstance(node.left, ast.Constant):
                    assignment_type = type(node.left.value).__name__
                elif isinstance(node.right, ast.Constant):
                    assignment_type = type(node.right.value).__name__
                elif isinstance(node.left, ast.List):
                    assignment_type = List.__name__
                elif isinstance(node.right, ast.List):
                    assignment_type = List.__name__
                elif isinstance(node.left, ast.Dict):
                    assignment_type = Dict.__name__
                elif isinstance(node.right, ast.Dict):
                    assignment_type = Dict.__name__
                elif isinstance(node.left, ast.Call):
                    # TODO: Check imported types and check already resolved functions?

                    assignment_type = None
                elif isinstance(node.right, ast.Call):
                    # TODO: Check imported types and check already resolved functions?
                    assignment_type = None
                else:
                    # TODO: Look back at operations we have already looked at for the type? Resolving later for now
                    assignment_type = None

                # Check whether we are working with another binary operation
                if isinstance(node.left, ast.BinOp):
                    # Since we have another binary operation, we will use its right node for hashing
                    binary_operation = BinaryOperation(
                        left=resolve_name(node.left.right),
                        left_ast_type=type(node.left.right),
                        right=resolve_name(node.right),
                        right_ast_type=type(node.right),
                        operator=type(node.op),
                        shared_type=assignment_type
                    )
                else:
                    # Not between two binary operations
                    binary_operation = BinaryOperation(
                        left=resolve_name(node.left),
                        left_ast_type=type(node.left),
                        right=resolve_name(node.right),
                        right_ast_type=type(node.right),
                        operator=type(node.op),
                        shared_type=assignment_type
                    )
                binary_operator_map.append(binary_operation)

        return binary_operator_map


class HeuristicParser(ast.NodeVisitor):
    """
    A heuristic NodeVisitor for assisting type inference
    """
    def __init__(self, node):
        self.node = node
        self.assign_nodes = []
        self.import_nodes = []
        self.records = []
        self.class_obj = {}
        self.alias_pair = []
        self.type_hint_pairs = []
        self.bo_test = []
        self.func_arg_db = {}
        self.call_links = []
        self.id2call = {}

    def _get_assign_records(self, node):
        id2call = {}
        for tmp_node in ast.walk(node):
            if isinstance(tmp_node, ast.Assign) and len(tmp_node.targets) == 1:
                left = tmp_node.targets[0]
                right = tmp_node.value
                if isinstance(left, ast.Name) and isinstance(right, ast.Call):
                    func_name = get_func_calls(right)[0]
                    id2call[left.id] = func_name
        all_func_names = get_func_calls(node)
        for func_name in all_func_names:
            if func_name in id2call:
                # This function call is a value of an assignment
                self.type_hint_pairs += [(id2call[func_name], "callable")]

    def visit_FunctionDef(self, node):
        self._get_assign_records(node)
        function_arg_types = get_call_type(node)
        for pair in function_arg_types:
            name, arg_type = pair
            if name in self.func_arg_db:
                self.func_arg_db[name] += [arg_type]
            else:
                self.func_arg_db[name] = [arg_type]
        self.generic_visit(node)

        return node

    def visit_Import(self, node):
        self.import_nodes.append(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.import_nodes.append(node)
        self.generic_visit(node)

    # Heuristic 4
    def visit_While(self, node):
        if isinstance(node.test, ast.Call):
            func_name = get_func_calls(node.test)
            func_name = func_name[0]
            self.bo_test += [func_name]
        self.generic_visit(node)

        return node

    # Heuristic 5
    def visit_Compare(self, node):
        left = node.left
        right = node.comparators[0]
        left_type = get_type(left)
        right_type = get_type(right)
        if left_type not in ["unknown", "ID", "subscript", "attr"] and right_type == "call":
            self.type_hint_pairs += [(get_func_calls(right)[0], left_type)]

        if right_type not in ["unknown", "ID", "subscript", "attr"] and left_type == "call":
            self.type_hint_pairs += [(get_func_calls(left)[0], right_type)]
        if left_type == "call" and right_type == "call":
            self.call_links = [(get_func_calls(left)[0],
                                get_func_calls(right)[0])]

        self.generic_visit(node)
        return node

    # Heuristic 5
    def visit_BinOp(self, node):
        left = node.left
        right = node.right
        left_type = get_type(left)
        right_type = get_type(right)
        if left_type not in ["unknown", "ID", "subscript", "attr"] and right_type == "call":
            self.type_hint_pairs += [(get_func_calls(right)[0], left_type)]

        if right_type not in ["unknown", "ID", "subscript", "attr"] and left_type == "call":
            self.type_hint_pairs += [(get_func_calls(left)[0], right_type)]

        if left_type == "call" and right_type == "call":
            self.call_links = [(get_func_calls(left)[0], get_func_calls(right)[0])]

        self.generic_visit(node)
        return node

    # Heuristic 4
    def visit_IfExp(self, node):
        if isinstance(node.test, ast.Call):
            func_name = get_func_calls(node.test)
            func_name = func_name[0]
            self.type_hint_pairs += [(func_name, "bool")]
        self.generic_visit(node)
        return node

    # Heuristic 4
    def visit_If(self, node):
        if isinstance(node.test, ast.Call):
            func_name = get_func_calls(node.test)
            func_name = func_name[0]
            self.bo_test += [func_name]
            self.type_hint_pairs += [(func_name, "bool")]
        self.generic_visit(node)
        return node


class SourceSplitVisitor(ast.NodeVisitor):
    """
    ast NodeVisitor class for retrieving assignments
    """
    def __init__(self):
        self.assign_dict = {}

    def visit_Assign(self, node):
        """
        When visit Assign, add information to the assignment dictionary
        Args:
            ast_node_lst: a list of statements to be visited.
            def_records: a list of dictionary, each of whose entry is a
            function/class definition.
            scope: the scope that is currently being visited. When it is "mod",
            it is visiting under the entire module.

        """
        if len(node.targets) > 1:
            return node
        left = node.targets[0]
        right = node.value
        if not isinstance(left, ast.Name):
            return node
        if left.id not in self.assign_dict:
            self.assign_dict[left.id] = [right]
        else:
            self.assign_dict[left.id] += [right]
        return node

    def visit_FunctionDef(self, node):
        return node


class ClassSplitVisitor(ast.NodeVisitor):
    """
    ast NodeVisitor class for retrieving compositions of a class: function nodes, bases and assignment records
    """
    def __init__(self):
        self.fun_nodes = []
        self.class_assign_records = {"init_arg_name_lst": []}
        self.bases = []

    def visit_FunctionDef(self, node):
        self.fun_nodes.append(node)
        if node.name == '__init__':
            for arg in node.args.args:
                self.class_assign_records["init_arg_name_lst"] += [arg.arg]
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Attribute):
                    left = get_attr_name(stmt.targets[0])
                    if left not in self.class_assign_records:
                        self.class_assign_records[left] = [stmt.value]
        return node

    def visit_ClassDef(self, node):
        self.bases = []
        for n in node.bases:
            if not isinstance(n, ast.Attribute) and not isinstance(n, ast.Subscript):
                if hasattr(n, 'id'):
                    self.bases.append(n.id)

        for tmp_node in node.body:
            if not isinstance(tmp_node, ast.Assign):
                continue
            if len(tmp_node.targets) > 1:
                continue
            left = tmp_node.targets[0]
            right = tmp_node.value
            if isinstance(left, ast.Name):
                if left.id not in self.class_assign_records:
                    self.class_assign_records[left.id] = [right]
                else:
                    self.class_assign_records[left.id] += [right]
            else:
                pass  # what if it is self.xxx like  TBD
        self.generic_visit(node)


class ReturnStmtVisitor(ast.NodeVisitor):
    """
    Class for inferring function return types
    """
    def __init__(self, imports=None, assignments=None):
        self.ast_nodes = []
        self.assign_records = {}
        self.local_assign_records = {}
        self.class_assign_records = {"init_arg_name_lst": []}
        self.inner_fun_names = []
        self.stem_from = []
        self.n_returns = 0
        self.r_types = []
        self.init_args = []
        self.imports = imports  # Dictionary of imported names and their types
        self.assignments = assignments  # List of variable assignment in a code block

    def import_assign_records(self, assign_records):
        """
        Import assignment records for return type inference
        Args:
            assign_records: a list of assignment records.
        """
        self.assign_records = assign_records

    def import_class_assign_records(self, assign_records):
        """
        Import class assignment records for return type inference
        Args:
            assign_records: a list of assignment records in the class.
        """
        self.class_assign_records = assign_records

    def import_assignments(self, assignments):
        self.assignments = assignments

    def visit_FunctionDef(self, node):
        args = node.args
        for arg in args.args:
            self.args.append(arg.arg)
        for tmp_node in ast.walk(node):
            if not isinstance(tmp_node, (ast.Assign, ast.AnnAssign)):
                continue

            left, right = None, None
            if isinstance(tmp_node, ast.Assign):
                if len(tmp_node.targets) == 1:
                    left = tmp_node.targets[0]
                    right = tmp_node.value
                else:
                    continue
            if isinstance(tmp_node, ast.AnnAssign):
                left = tmp_node.target
                right = tmp_node.value

            if isinstance(left, ast.Name):
                if left.id not in self.local_assign_records:
                    self.local_assign_records[left.id] = [right]
                else:
                    self.local_assign_records[left.id] += [right]

            if isinstance(left, ast.Attribute):
                left_name = get_attr_name(left)
                if left_name not in self.local_assign_records:
                    self.local_assign_records[left_name] = [right]
                else:
                    self.local_assign_records[left_name] += [right]
            else:
                pass  # what if it is self.xxx like  TBD
        self.type_infer_CFG(node)
        return node

    def visit_Yield(self, node):
        self.n_returns += 1
        self.r_types += ['generator']
        return node

    def infer_actual_return_value(self, actual_return_value):
        """
        Infer the return type with the help of assignment records and the possible return values
        Args:
            assign_records: a list of assignment records.
        """
        # actual value means the value that has been traced back
        is_visited = set()

        if actual_return_value is None:
            self.r_types += ["empty"]
            return
        elif isinstance(actual_return_value, ast.Name):
            if actual_return_value.id == "self":
                self.r_types += ["self"]
                return
            elif actual_return_value.id in self.inner_fun_names:
                # TODO: What about outer fun names or class methods
                self.r_types += ["callable"]
                return

        init_val = actual_return_value #
        type_val = get_type(init_val, imports=self.imports)

        if init_val is None and isinstance(actual_return_value, ast.Name):
            if return_value.id in self.args:
                self.r_types += ['input']
            if return_value.id in self.args:
                self.r_types += ['input']
                return

        if isinstance(actual_return_value, ast.Name):
            # Check to see if we have the return in our list of assignments
            for assignment in self.assignments:
                if assignment.name == actual_return_value.id:
                    self.r_types += [assignment.type]
            return

        if isinstance(actual_return_value, ast.BinOp):
            heuristics = Heuristics()
            return_type = heuristics.heuristic_five_return(
                assignments=self.assignments,
                return_node=actual_return_value
            )
            if isinstance(return_type, list):
                for type in return_type:
                    self.r_types.append(type)
            else:
                self.r_types += [return_type]
            return

        if type_val in ["ID", "attr"]:
            # TODO: Is block.id correct here?
            if type_val == 'attr' and isinstance(init_val.value, ast.Call):
                # Check for super class call
                if not isinstance(init_val.value.func, ast.Attribute):
                    if init_val.value.func.id == 'super':
                        # Check super class attributes
                        attribute_name = f"super.{init_val.attr}"
                        super_assign = self.class_assign_records.get(attribute_name)
                        if super_assign:
                            type_val = get_type(super_assign[0])

            lookup_name = block.id if type_val == "ID" else get_attr_name(init_val)
            if lookup_name in self.local_assign_records:
                right = self.local_assign_records[lookup_name][-1]
                self.type_infer(right)
            elif lookup_name.lstrip("self.") in self.class_assign_records:
                right = self.class_assign_records[lookup_name[5:]][-1]
                self.type_infer(right)
                # use self.name again
            elif lookup_name in self.class_assign_records:
                right = self.class_assign_records[lookup_name][-1]
                self.type_infer(right)

            elif lookup_name in self.assign_records:
                # TBD inspect
                right = self.assign_records[lookup_name][-1]
                self.type_infer(right)
            else:
                pass
        elif type_val == "call":
            func_name = get_func_calls(actual_return_value)
            func_name = func_name[0]
            first_part = func_name.split('.')[0]
            if func_name == "self.__class__":
                # same as class itself
                self.r_types += ['self']
            elif first_part != 'self' and first_part in self.args:
                self.r_types += ['input']
            elif first_part != 'self' and first_part in self.class_assign_records["init_arg_name_lst"]:
                self.r_types += ['input']
            else:
                self.stem_from.append(func_name)

        elif type_val == "subscript":
            if isinstance(init_val, ast.Name):
                if init_val.id in self.args or init_val.id in self.class_assign_records["init_arg_name_lst"]:
                    self.r_types += ['input']
            else:
                # Can't deduce type, return Any
                self.r_types += [any.__name__]

        else:
            # Known type
            self.r_types += [type_val]

    def type_infer_CFG(self, node):
        """
        Conduct SSA analysis in CFG to get the possible return values
        Args:
            assign_records: a list of assignment records.
        """
        new_body = []
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                self.inner_fun_names.append(stmt.name)
            elif isinstance(stmt, ast.ClassDef):
                self.inner_fun_names.append(stmt.name)
            else:
                for small_stmt in ast.walk(stmt):
                    if isinstance(small_stmt, ast.Return):
                        self.n_returns += 1
                    elif isinstance(small_stmt, ast.Yield):
                        self.n_returns += 1
                        self.r_types += ["generator"]
                new_body.append(stmt)

        tmp_fun_node = ast.Module(body=new_body)
        cfg = CFGBuilder().build(node.name, tmp_fun_node)

        ssa_analyzer = SSA()
        ssa_results, ident_const_dict = ssa_analyzer.compute_SSA(cfg)
        def get_return_value(block):
            for idx, stmt in enumerate(block.statements):
                if isinstance(stmt, (ast.Return, ast.Yield)):
                    # when possible assignment can be found.
                    if isinstance(stmt.value, ast.Name):
                        stmt_loaded_rec = ssa_results[block.id][idx]
                        # use the first value
                        # TODO: consider multiple return values
                        ident_all_numbers = set(stmt_loaded_rec[stmt.value.id])
                        if len(ident_all_numbers)>0:
                            const_values = []
                            for ident_no in ident_all_numbers:
                                const_values.append(ident_const_dict[stmt.value.id, ident_no])
                            return const_values
                    # this includes the case when the return identifier cannot be traced to a definition
                    return [stmt.value]
            return None

        for block in cfg.finalblocks:
            return_values = get_return_value(block)
            if return_values:
                for return_value in return_values:
                    self.infer_actual_return_value(return_value)
                    #print(block.statements[0].lineno)
                    #print(self.r_types)




            #if isinstance(return_value, ast.IfExp):

            #    self.backward(cfg, block, return_value.body)
            #    self.backward(cfg, block, return_value.orelse)
            #else:
            #    self.backward(cfg, block, return_value)

    def query_assign_records(self, var_id):
        if var_id in self.local_assign_records:
            # this includes alias analysis
            right = self.local_assign_records[var_id][-1]
            return right
        elif var_id in self.class_assign_records:
            right = self.class_assign_records[var_id][-1]
            return right
            # self.type_infer(right)
        elif var_id in self.assign_records:
            # TBD inspect
            right = self.assign_records[var_id][-1]
            return right
            # self.type_infer(right)
        return None

    def type_infer(self, node):
        # if node is None, return None??
        type_val = get_type(node)
        if type_val == 'ID':
            right = self.query_assign_records(node.id)
            if right is not None:
                self.type_infer(right)
            else:
                pass
        elif type_val == 'call':
            # Returns a function call
            func_name = get_func_calls(node)
            func_name = func_name[0]
            first_part_name = func_name.split('.')[0]

            if first_part_name in self.args or first_part_name in self.class_assign_records["init_arg_name_lst"]:
                self.r_types += ['input']
            elif func_name in self.args:
                self.r_types += ['input']
            elif func_name in self.class_assign_records["init_arg_name_lst"]:
                self.r_types += ['input']
            elif func_name in ['copy', 'deepcopy', 'copy.copy', 'copy.deepcopy']:
                pass
            else:
                self.stem_from.append(func_name)  # if this is a function call # self.r_types += [type_val]
        elif type_val == "subscript":
            if isinstance(node.value, ast.Name) and node.value.id in self.args:
                self.r_types += ['input']
        else:
            # Known type
            self.r_types += [type_val]

    def clear(self):
        self.r_types = []
        self.n_returns = 0
        self.args = []  # TODO: Resolve
        self.stem_from = []
        self.ast_nodes = []
        self.inner_fun_names = []
        self.local_assign_records = {}

    def clear_all(self):
        self.clear()
        self.class_assign_records = {}


class Heuristics:
    """
    A set of heuristic function for assisting type inference
    """
    @staticmethod
    def heuristic_two(ast_tree, processed_file, assignments):
        """
        Args:
            ast_tree: the root node of the ast tree
            processed_file: the files that have been processed
            assignments: the assignment list
        """
        function_param_types = {}
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                func_args = node.args.args
                func_name = node.name
                function_param_types[func_name] = [{
                    "possible_arg_types": [],
                    "funcs": [],
                    "type": "",
                    "param_name": x.arg
                } for x in func_args
                ]

            elif hasattr(node, "value") and isinstance(node.value, ast.Call):

                if isinstance(node.value.func, ast.Attribute) or isinstance(node.value.func, ast.Name):
                    continue

                if hasattr(node.value.func, 'id'):
                    func_name = node.value.func.id
                    args = node.value.args
                    for i in range(len(args)):
                        arg = args[i]
                        if isinstance(arg, ast.Call):
                            function_param_types[func_name][i]["funcs"].append(arg.func.id)
                        elif isinstance(arg, ast.Name):
                            pass
                        else:
                            function_param_types[func_name][i]["possible_arg_types"].append(type(arg.value).__name__)

        for function in function_param_types.values():
            for arg in function:
                param_name = arg["param_name"]
                possible_types = list(set(arg["possible_arg_types"]))
                if len(possible_types) == 1:
                    arg["type"] = possible_types[0]

        for static_assignment in processed_file.static_assignments:
            function_name = static_assignment.function
            parameter_name = static_assignment.name
            if function_name in function_param_types:
                for arg in function_param_types[function_name]:
                    if arg["param_name"] == parameter_name:
                        if arg["type"] is not None and arg["type"] != "":
                            static_assignment.type = arg["type"]

    def heuristic_five(self, import_mappings, processed_file, function_node):
        """
        Args:
            import_mappings: the import mappings that have been generated
            processed_file: the files that have been processed
            function_node: the function node being checked
        """
        # Perform heuristic five within a function

        param_list = [v for v in processed_file.static_assignments if v.is_arg]
        assignment_dict = {v.name: v for v in processed_file.static_assignments}
        for variable in list(reversed(processed_file.static_assignments)):
            if variable.binary_operation is not None:
                # Get left and right for the binary operation
                left_operation = variable.binary_operation.left
                right_operation = variable.binary_operation.right
                operation = variable.binary_operation.op
                # Check for involved parameters
                involved_params = [i for i in param_list if self.in_bin_op(i, variable.binary_operation)]

                if isinstance(left_operation, ast.BinOp):
                    # Greater than two values in the operation
                    bin_op_types = {}
                    while isinstance(left_operation, ast.BinOp):

                        if isinstance(right_operation, ast.Name):
                            # Named variable
                            if isinstance(left_operation.right, ast.Name):
                                right_name = left_operation.right.id
                                right_variable = assignment_dict.get(right_name)
                                if right_variable:
                                    bin_op_types[right_variable.type] = True
                            elif isinstance(left_operation.right, ast.Constant):
                                bin_op_types[type(left_operation.right.value).__name__] = True
                        elif isinstance(right_operation, ast.Constant):
                            # Constant value, e.g. 25 as an integer of 'Hello World!' as a string
                            bin_op_types[type(right_operation.value).__name__] = True
                        # Move to next left operation
                        left_operation = left_operation.left

                    # Check type list for types
                    if len(bin_op_types.keys()) == 1:
                        type_value = list(bin_op_types.keys()).pop()
                        variable.type = type_value
                        # Set involved parameters types
                        for i in involved_params:
                            i.type = type_value
                    else:
                        # TODO: Check for compatible types e.g. float and str
                        # TODO: Check for mismatched types and raise error
                        pass

                else:
                    # Check left
                    if isinstance(left_operation, ast.Name):
                        left_name = left_operation.id
                        left_variable = assignment_dict.get(left_name)
                        if left_variable:
                            variable.type = left_variable.type
                    elif isinstance(left_operation, ast.Constant):
                        variable.type = type(left_operation.value).__name__

                    # Check right
                    if isinstance(right_operation, ast.Name):
                        right_name = right_operation.id
                        right_variable = assignment_dict.get(right_name)
                        if right_variable:
                            if right_variable.type == "any" \
                                    and (isinstance(operation, ast.Pow) or isinstance(operation, ast.Mod)):
                                variable.type = "float"
                            else:
                                variable.type = right_variable.type
                    elif isinstance(right_operation, ast.Constant):
                        variable.type = type(right_operation.value).__name__

    def heuristic_five_return(self, assignments, return_node: ast.BinOp):
        # Perform heuristic five on a returned binary operation
        involved = self.get_bin_op_involved(return_node)

        # Check involved for known types
        for i in involved:
            if isinstance(i, ast.Name):
                # Named variable, see if it is a known type
                assignment_dict = {v.name: v for v in assignments}
                assignment = assignment_dict.get(i.id)
                if assignment:
                    if assignment.type != 'any':
                        return assignment.type
            elif isinstance(i, ast.Constant):
                # Constant, check its type
                return type(i.value).__name__

        # If we are here we've returned nothing
        if hasattr(return_node, "op"):
            operation = return_node.op
            number_operations = [ast.Pow, ast.Mod]
            if any([isinstance(operation, x) for x in number_operations]):
                return "float"
        else:
            return "any"

    @staticmethod
    def heuristic_six(processed_file, function_node):
        """
        Args:
            processed_file: the files that have been processed
            function_node: the function node being checked
        """
        function_calls = []
        for node in ast.walk(function_node):
            # Visit ast.Call nodes, checking for variable names
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    function_calls.append(node.func.id)

        # Get variables that are called
        involved = [v for v in processed_file.static_assignments if v.name in function_calls]
        for variable in involved:
            variable.type = callable.__name__

    @staticmethod
    def heuristic_seven(processed_file, function_node):
        """
        Args:
            processed_file: the files that have been processed
            function_node: the function node being checked
        """
        # Track calls to isinstance()
        is_instance_type_map = {}
        for node in ast.walk(function_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == 'isinstance':
                        # Check to see what the value being compared to is
                        variable, type_compared = node.args[0], node.args[1]
                        if isinstance(variable, ast.Name) and isinstance(type_compared, ast.Name):
                            type_list = is_instance_type_map.get(variable.id)
                            if type_list:
                                if type_compared.id not in type_list:
                                    type_list.append(type_compared.id)
                            else:
                                is_instance_type_map[variable.id] = [type_compared.id]

        # Check static assignments for the variables involved in calls to isinstance
        involved = [s for s in processed_file.static_assignments if s.name in is_instance_type_map]
        for variable in involved:
            is_instance_types = is_instance_type_map[variable.name]

            # Variable hasn't been resolved by any other heuristics
            if variable.type == 'any':
                if len(is_instance_types) > 1:
                    variable.type = is_instance_types
                else:
                    variable.type = is_instance_types[0]

    @staticmethod
    def heuristic_eight(ast_tree, function_name, function_params):
        """
        Performs heuristic 8 for a function's inputs. Note that this heuristic
        attempts to infer/check the types a developer likely intended for function
        parameters and provide a limited number of types to the actual number that
        may work
        Args:
            ast_tree: The ast tree for the module the function is in
            function_name: The name of the function being checked
            function_params: The function parameters from a variable assignment map
        """
        param_type_map = {p.name: {} for p in function_params}
        param_map = {p.name: p for p in function_params}

        # Collect parameter input types
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == function_name:
                        inputs = [n.value for n in node.args if hasattr(n, "value")]
                        if len(inputs) == len(function_params):
                            for index, param in enumerate(function_params):
                                param_type_map[param.name][type(inputs[index]).__name__] = True

        # Assign parameter input types to parameters
        for param_name, param_types in param_type_map.items():
            parameter = param_map.get(param_name)
            type_values = list(param_types.keys())
            if len(type_values) == 1:
                # Validate
                if parameter.type == 'any':
                    parameter.type = type_values[0]
                elif not param_types.get(parameter.type):
                    # Mismatched inferred types
                    # TODO: Raise a warning here?
                    pass

            else:
                # See if we already inferred type from another heuristic, and check against the input type
                if parameter.type != 'any':
                    if parameter.type not in type_values:
                        # Bad input to function
                        # TODO: Raise a warning here?
                        pass
                    # TODO: Raise warning for types that are passed as input incorrectly?
                elif len(type_values) > 0:
                    # Couldn't infer type from other heuristic, set as union of passed in types
                    parameter.type = type_values

    @staticmethod
    def heuristic_nine(import_mappings, processed_file, function_node):
        """
        Args:
            import_mappings: The import mappings that have been generated
            processed_file: The files that have been processed
            function_node: The function node being checked
        """
        # work through params
        for variable in [v for v in processed_file.static_assignments if v.type == 'any']:
            regex_query = r'\b^(.{0,12}_{0,1}(count|counter|sum)_{0,1}.{0,12}|(int|num|sum|count|counter))$\b'
            regex = re.search(regex_query, variable.name)
            if regex:
                variable.type = 'int'

    def heuristic_eleven(self, processed_file, function_node):
        # Find what variables are in comparison operations and resolve types
        pass

    @staticmethod
    def heuristic_twelve(function_node, function_params):
        """
        Performs heuristic 8 for a function's inputs. Note that this heuristic
        attempts to infer/check the types a developer likely intended for function
        parameters and provide a limited number of types to the actual number that
        may work
        Args:
            ast_tree: The ast tree for the module the function is in
            function_name: The name of the function being checked
            function_params: The function parameters from a variable assignment map
        """
        param_type_map = {p.name: {} for p in function_params}
        param_map = {p.name: p for p in function_params}

        # Collect parameter input types
        args = function_node.args
        kwarg = args.kwarg
        kw_defaults=args.kw_defaults
        defaults = args.defaults
        position = 0
        if len(defaults)>0 :
            for arg in list(param_type_map.keys())[-len(defaults):]:
                # None is not helpful, not providing any hint
                if hasattr(defaults[position], "value"):
                    if defaults[position].value is not None:
                        param_type_map[arg][type(defaults[position].value).__name__] = True
                        position+=1

        # Assign parameter input types to parameters
        for param_name, param_types in param_type_map.items():
            parameter = param_map.get(param_name)
            type_values = list(param_types.keys())
            if len(type_values) == 1:
                # Validate
                if parameter.type == 'any':
                    parameter.type = type_values[0]
                elif not param_types.get(parameter.type):
                    # Mismatched inferred types
                    # TODO: Raise a warning here?
                    pass

            else:
                # See if we already inferred type from another heuristic, and check against the input type
                if parameter.type != 'any':
                    if parameter.type not in type_values:
                        # Bad input to function
                        # TODO: Raise a warning here?
                        pass
                    # TODO: Raise warning for types that are passed as input incorrectly?
                elif len(type_values) > 0:
                    # Couldn't infer type from other heuristic, set as union of passed in types
                    parameter.type = type_values

    @staticmethod
    def get_bin_op_involved(binary_operation: ast.BinOp):
        """
        Get list of variables/constants/callables involved in a binary operation
        Args:
            binary_operation: the binary operation to get the names for
        Returns:
            List: list of variable/constants/callables
        """
        involved = []
        left_operation = binary_operation.left
        right_operation = binary_operation.right
        involved.append(right_operation)
        if isinstance(left_operation, ast.BinOp):
            # Greater than two values in the operation
            while isinstance(left_operation, ast.BinOp):
                involved.append(left_operation.right)
                # Move to next left operation
                left_operation = left_operation.left
        involved.append(left_operation)
        return involved

    @staticmethod
    def in_bin_op(variable: ScalpelVariable, binary_operation: ast.BinOp):
        """
        Determines whether a variable is featured in a binary operation
        Args:
            variable: The variable to check for
            binary_operation: The binary operation to check
        Returns:
            Boolean: True if it is within the binary operation, false otherwise
        """
        left_operation = binary_operation.left
        right_operation = binary_operation.right
        if isinstance(left_operation, ast.BinOp):
            # Greater than two values in the operation
            while isinstance(left_operation, ast.BinOp):
                if isinstance(left_operation.right, ast.Name):
                    right_name = left_operation.right.id
                    if right_name == variable.name:
                        return True
                # Move to next right operation
                left_operation = left_operation.left
        if isinstance(left_operation, ast.Name):
            if left_operation.id == variable.name:
                return True
        if isinstance(right_operation, ast.Name):
            if right_operation.id == variable.name:
                return True
        return False
