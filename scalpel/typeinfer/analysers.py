"""
Tomas Bolger 2021
Python 3.9
Scalpel Type Inference Static Analysis Tools
"""

import ast
import tokenize
import typed_ast
import typeshed_client
from typing import List, Dict

from scalpel.cfg import CFGBuilder
from scalpel.typeinfer.classes import BinaryOperation, ScalpelVariable, ScalpelFunction, ScalpelClass
from scalpel.typeinfer.visitors import get_func_calls_type as get_func_calls, get_call_type
from scalpel.typeinfer.utilities import (
    get_type,
    get_attr_name,
    get_built_in_types,
    resolve_name
)


class BinaryOperatorMap:

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
        if hashed := self.hash.get(item):
            return hashed
        return None

    def chain_types(self):
        """
        TODO: Chain together types of variables involved in binary operations to determine types
        """
        for variable, operation_list in self.hash.items():
            if isinstance(self._type_hash.get(variable), ast.Constant):
                pass


class _StaticAnalyzer(ast.NodeVisitor):
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

        :param file_name: The name of the file to read
        :type file_name: str
        :return: The read file tokens
        """
        with tokenize.open(file_name) as file:
            return file.read()


class ImportTypeMap(_StaticAnalyzer):
    """
    Class for mapping import types
    """

    def __init__(self, root):
        super().__init__()
        self.imports: Dict[str, str] = {}
        self.typeshed_resolver = typeshed_client.Resolver()
        self.root = root

    def map(self):
        import_mappings = {}  # Maps imported functions, variables, etc. to their types
        imports = {}  # Keeps a dictionary of imported libraries
        for node in ast.iter_child_nodes(self.root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):
                module = node.module.split('.')
            else:
                continue

            for names in node.names:
                for name in names.name.split('.'):
                    import_name = ".".join(module + [name])
                    if module:
                        # Importing from module
                        import_type = self.get_imported_type(import_name)
                        import_mappings[name] = import_type
                    else:
                        # Importing whole module
                        imports[import_name] = True

        return import_mappings, imports

    def get_imported_type(self, import_name: str):
        fully_qualified_name = self.typeshed_resolver.get_fully_qualified_name(import_name)
        if isinstance(fully_qualified_name, typeshed_client.parser.NameInfo):
            node = fully_qualified_name.ast
            if isinstance(node, typed_ast._ast3.FunctionDef):
                if isinstance(node.returns, typed_ast._ast3.Subscript):
                    return node.returns.value.id
                return node.returns.id
            elif isinstance(node, typed_ast._ast3.AnnAssign):
                return node.annotation.id
            elif isinstance(node, typed_ast._ast3.ClassDef):
                return node.name  # Type is class name
        return 'any'


class ClassDefinitionMap(_StaticAnalyzer):
    """
    Class for retrieving class definitions in a file
    """

    def __init__(self, root):
        super().__init__()
        self.root = root

    def map(self) -> List[ScalpelClass]:
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
        super().__init__()
        self.root = root

    def map(self) -> List[ScalpelFunction]:
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
        super().__init__()
        if imports is None:
            imports = {}
        self.root = root
        self.imports = imports  # Pass in the imported types for a files

    def map(self) -> List[ScalpelVariable]:
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

                variable_name = node.targets[0].id
                assignment_type = any.__name__

                variable = ScalpelVariable(
                    name=variable_name,
                    function="",
                    line=node.lineno,
                    type=assignment_type
                )
                if isinstance(node.value, ast.Call):
                    # Assignment is to a callable
                    called = node.value.func.id  # Name of callable

                    # Check to see if it is an imported callable
                    if imported_type := self.imports.get(called):
                        variable.type = imported_type

                elif isinstance(node.value, ast.Constant):
                    # String, int, float, boolean
                    variable.type = type(node.value.value).__name__  # Determine specific type
                elif isinstance(node.value, ast.Dict):
                    # Dictionary
                    key_type = self.__check_consistent_list_types(node.value.keys)
                    value_type = self.__check_consistent_list_types(node.value.values)
                    variable.type = f"Dict[{key_type}, {value_type}]"
                elif isinstance(node.value, ast.List) or isinstance(node.value, ast.Tuple):
                    # List or tuple, check to see if types in list are constant
                    values = node.value.elts
                    value_type = self.__check_consistent_list_types(values)
                    variable.type = f"{type(node.value).__name__}[{value_type}]"
                elif isinstance(node.value, ast.IfExp) or isinstance(node.value, ast.Compare):
                    # Boolean, see heuristic 4
                    variable.type = bool.__name__
                elif isinstance(node.value, ast.BinOp):
                    # Assignment to result of binary operation
                    variable.binary_operation = node.value
                variables.append(variable)

        return variables

    @staticmethod
    def __check_consistent_list_types(values) -> str:
        """
        Checks a list of values to see if they have a constant type
        """
        if len(values) == 0:
            # Nothing in list yet so return any
            return any.__name__
        first_type = type(values[0])
        assignment_type = any.__name__
        if not first_type == ast.Constant:
            builtin_types_dict = get_built_in_types()
            builtin_first_type = builtin_types_dict.get(first_type.__name__.lower())
            # Not an AST constant so we can just compare AST types
            for n in values[1:len(values)]:
                # Compare type to first items type
                if not isinstance(n, first_type):
                    # No constant type, assign any
                    assignment_type = any.__name__
                    break
                else:
                    assignment_type = builtin_first_type
        else:
            # We have an AST constant so we will need to compare their types
            first_constant_type = type(values[0].value)
            assignment_type = first_constant_type.__name__
            for n in values[1:len(values)]:
                # Compare type to first items type
                if not isinstance(n, ast.Constant):
                    # Not a constant type, assign any
                    assignment_type = any.__name__
                    break
                else:
                    if not isinstance(n.value, first_constant_type):
                        assignment_type = any.__name__
                        break
        return assignment_type


class BinaryOperationMap(_StaticAnalyzer):
    """
    Class for retrieving variable assignments
    """

    def __init__(self, root):
        super().__init__()
        self.root = root

    def map(self) -> BinaryOperatorMap:

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
    def __init__(self):
        self.assign_dict = {}

    def visit_Assign(self, node):
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
    def __init__(self):
        self.fun_nodes = []
        self.class_assign_records = {"init_arg_name_lst": []}

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
        self.assign_records = assign_records

    def import_class_assign_records(self, assign_records):
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

    @staticmethod
    def get_return_value(block):
        for stmt in block.statements:
            if isinstance(stmt, ast.Return):
                return stmt.value
        return None

    # input: the object to be back traced
    def backward(self, cfg, block, return_value):
        is_visited = set()

        if return_value is None:
            self.r_types += ["empty"]
            return
        elif isinstance(return_value, ast.Name):
            if return_value.id == "self":
                self.r_types += ["self"]
                return
            elif return_value.id in self.inner_fun_names:
                # TODO: What about outer fun names or class methods
                self.r_types += ["callable"]
                return

        init_val = cfg.backward(block, return_value, is_visited, None)
        type_val = get_type(init_val, imports=self.imports)

        if init_val is None and isinstance(return_value, ast.Name):
            if return_value.id in self.args:
                self.r_types += ['input']
            if return_value.id in self.args:
                self.r_types += ['input']
                return

        if isinstance(return_value, ast.Name):
            # Check to see if we have the return in our list of assignments
            for assignment in self.assignments:
                if assignment.name == return_value.id:
                    self.r_types += [assignment.type]
            return

        if type_val in ["ID", "attr"]:
            # TODO: Is block.id correct here?
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
            func_name = get_func_calls(init_val)
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
            # Known type
            self.r_types += [type_val]

    def type_infer_CFG(self, node):
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

        for block in cfg.finalblocks:
            return_value = self.get_return_value(block)
            if isinstance(return_value, ast.IfExp):
                self.backward(cfg, block, return_value.body)
                self.backward(cfg, block, return_value.orelse)
            else:
                self.backward(cfg, block, return_value)

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
