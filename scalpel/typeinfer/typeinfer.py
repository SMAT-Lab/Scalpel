"""
Tomas Bolger 2021
Python 3.9
Scalpel Type Inference Module
"""

import os
import ast
import tokenize
import typed_ast
import typeshed_client
from pprint import pprint
from dataclasses import dataclass
from typing import List, Dict, Union

from scalpel.cfg import CFGBuilder

import utilities

builtin_types_dict = utilities.get_built_in_types()


@dataclass
class TypeWarning:
    warning: str  # Stores warning text
    line: int  # Line number of warning
    file: str  # Line where the warning was found
    variable: str  # Name of the variable

    def print_warning(self):
        print(f"{self.file}:{self.line}: {self.warning}")


@dataclass
class ScalpelVariable:
    name: str  # The name of the variable
    function: str  # The name of the function where the variable is defined
    line: int  # The line number that the variable is defined at
    type: str = None  # The type of the variable as a string
    in_conditional: bool = False  # Whether the variable is involved in any conditional statements
    in_equality: bool = False  # Whether the variable is involved in an equality statement
    is_callable: bool = False  # Whether the variable has been called as a function
    called_methods: List[str] = None  # List of methods called from the variable
    binary_operations: Dict[str, str] = None  # Dictionary indexed by other variable name and the operator used


@dataclass
class ScalpelFunction:
    """
    Holds information about a function
    """
    name: str  # The name of the function
    line: int  # The line number that the variable is defined at
    return_type: str = None  # The return type of the function


@dataclass
class ScalpelClass:
    """
    Holds information about a class
    """
    name: str  # The name of the class
    methods: List[ScalpelFunction]  # List of functions defined in the class
    inherits: List[str] = None  # Name of the class that this class inherits from


@dataclass
class BinaryOperation:
    """
    Holds information about a binary operation between two variables
    """
    left: str  # The left variable
    left_ast_type: any  # The AST type of the left variable
    right: str  # The right variable
    right_ast_type: any  # The AST type of the right variable
    operator: any  # The binary operator used between the two variables
    shared_type: str = None  # Stores shared type between the variables in the operation


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

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.imports: Dict[str, str] = {}
        self.typeshed_resolver = typeshed_client.Resolver()
        self.root = ast.parse(_StaticAnalyzer.read_file(self.file_name))

    def map(self):
        # TODO: Add check in here to see if import is a local file, if it is
        #  we may have to recursively instantiate a type inference process on it
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

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.root = ast.parse(_StaticAnalyzer.read_file(self.file_name))

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

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.root = ast.parse(_StaticAnalyzer.read_file(self.file_name))

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

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.root = ast.parse(_StaticAnalyzer.read_file(self.file_name))

    def map(self) -> List[ScalpelVariable]:
        # TODO: Ensure coverage of all variable types
        variables = []
        for node in ast.walk(self.root):
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                # TODO: Look for ast.AugAssign node to check types are consistent
                variable_name = node.targets[0].id
                assignment_type = any.__name__
                if isinstance(node.value, ast.Call):
                    # Assignment is to a callable
                    called = node.value.func.id  # Name of callable

                elif isinstance(node.value, ast.Constant):
                    # String, int, float, boolean
                    assignment_type = type(node.value.value).__name__  # Determine specific type
                elif isinstance(node.value, ast.Dict):
                    # Dictionary
                    key_type = self.__check_consistent_list_types(node.value.keys)
                    value_type = self.__check_consistent_list_types(node.value.values)
                    assignment_type = f"Dict[{key_type}, {value_type}]"
                elif isinstance(node.value, ast.List) or isinstance(node.value, ast.Tuple):
                    # List or tuple, check to see if types in list are constant
                    values = node.value.elts
                    value_type = self.__check_consistent_list_types(values)
                    assignment_type = f"{type(node.value).__name__}[{value_type}]"
                elif isinstance(node.value, ast.IfExp) or isinstance(node.value, ast.Compare):
                    # Boolean, see heuristic 4
                    assignment_type = bool.__name__

                variables.append(ScalpelVariable(
                    name=variable_name,
                    function="",  # TODO: How to determine this easily? Line numbers?
                    line=node.lineno,
                    type=assignment_type
                ))

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

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.root = ast.parse(_StaticAnalyzer.read_file(self.file_name))

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


class TypeInference:
    """
    Infer types from a given AST node
    """

    def __init__(self, files: List[str]):
        self.files = files

    def infer_types(self, print_types=True) -> List[Dict]:
        """
        Returns dictionary with each variable in each method with what types it might be
        """
        # Run type inference process
        type_list = []
        for file_name in self.files:
            # Get some initial details for the file

            # Get imported types
            imported_types, imports = ImportTypeMap(file_name).map()

            # Get class definitions
            class_definitions = ClassDefinitionMap(file_name).map()

            # Get function definitions
            function_definitions = FunctionDefinitionMap(file_name).map()

            # Collect information about each variable assignment
            variables = VariableAssignmentMap(file_name).map()
            # For the variables we known the types of, create warnings for them
            for variable in variables:
                print(variable.name, variable.type)

            # Collection information about binary operations between variables
            binary_operations = BinaryOperationMap(file_name).map()

            # Create CFG
            cfg_builder = CFGBuilder()
            cfg = cfg_builder.build_from_file(
                name='Test',
                filepath=get_test_files()[0]
            )
            reversed_traversal = reversed([node for node in cfg])
            # for node in reversed_traversal:
            # print([n.lineno for n in node.statements])

        return [{}]

    def __resolve_function_return(self):
        pass


def resolve_name(node: any) -> Union[str, None]:
    """
    Resolve the string name of an AST node
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        # TODO: Attributes will have to be resolved to their classes, due to classes having same attribute names
        return node.attr
    elif isinstance(node, ast.Call):
        return node.func.id
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        return None


def get_test_files():
    # Get list of test files
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    test_file_dir = os.path.join(directory, 'test_files')
    test_files = []
    for f in os.listdir(test_file_dir):
        full_path = os.path.join(test_file_dir, f)
        test_files.append(os.path.relpath(full_path))
    return test_files


def test_type_inference():
    # Run type inference module on them
    type_inferrer = TypeInference(get_test_files())
    types = type_inferrer.infer_types()


if __name__ == '__main__':
    test_type_inference()
