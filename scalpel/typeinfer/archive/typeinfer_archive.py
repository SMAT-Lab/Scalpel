"""
Tomas Bolger 2021
Python 3.9
Type Inference by Static Analysis
"""

import os
import ast
import builtins
import tokenize
import typed_ast
import typeshed_client
from pprint import pprint
from typing import List, Dict
from dataclasses import dataclass
from collections import defaultdict

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


class _FunctionReturnInference(_StaticAnalyzer):
    """
    Attempts to infer function return type
    """

    # TODO: Track dictionary key value pair types
    # TODO: Track imports for variable types -> locate method type hints from stub files

    def __init__(self):
        super().__init__()
        self.function_return_map = defaultdict(set)

    def visit_FunctionDef(self, node):

        # Get imported types and libraries
        imported_types, imported_libraries = _MapImportTypes(self.file_name).map()

        for n in node.body:
            self.visit(n)
        # Used to track variable assigned types
        assignment_type_map = defaultdict(str)

        # Check to see if the function returns immediately
        n = node.body[0]
        if isinstance(n, ast.Return):
            if isinstance(n.value, ast.Call):
                pass
                # Check to see if it is an imported function
                #if return_type := imported_types.get(call_name):
                    #self.function_return_map[self.file_name].add((node.name, return_type, node.lineno, n.value.id))
        else:
            # Multiple nodes
            for i, n in enumerate(node.body):
                # Track variable assignment types
                if isinstance(n, ast.Return) and isinstance(n.value, ast.Name):
                    # Returning variable, check to see if we have its type
                    if return_type := assignment_type_map.get(n.value.id):
                        if builtin_type := builtin_types_dict.get(return_type.lower()):
                            # We have a builtin type, update function return map
                            self.function_return_map[self.file_name].add((node.name, builtin_type, node.lineno, n.value.id))
                        elif return_type in imported_types:
                            self.function_return_map[self.file_name].add((node.name, return_type, node.lineno, n.value.id))
                        else:
                            # Make return type any
                            self.function_return_map[self.file_name].add((node.name, 'any', node.lineno, n.value.id))
                else:
                    # Check for assignments
                    if isinstance(n, ast.Assign):
                        variable_name = n.targets[0].id
                        if isinstance(n.value, ast.Call):
                            # TODO: Get call return type
                            # Check to see if call is to external library, or within the file?
                            # If its a function in the file and we have its return type, we can infer from it since
                            # if f() returns g() and g() returns 'str', therefore f() returns 'str'

                            # Checking for reference to imported library
                            call_name = n.value.func.id
                            if call_type := imported_types.get(call_name):
                                assign_type = call_type
                            else:
                                assign_type = any.__name__
                        elif isinstance(n.value, ast.Constant):
                            assign_type = type(n.value.value).__name__
                        else:
                            assign_type = type(n.value).__name__
                        assignment_type_map[variable_name] = assign_type

    def report(self) -> List[TypeWarning]:
        warnings = []
        for path, function_returns in self.function_return_map.items():
            for function_name, return_type, line, variable in function_returns:
                warnings.append(TypeWarning(
                    warning=f"Function {function_name}() has return type '{return_type}'",
                    line=line,
                    file=path,
                    variable=variable
                ))
        return warnings


class _MapImportTypes:
    """
    Class to map the import types of a file
    """

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.imports: Dict[str, str] = {}
        self.typeshed_resolver = typeshed_client.Resolver()
        self.root = ast.parse(_StaticAnalyzer.read_file(self.file_name))

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


class TypeInference:
    """
    Infer types from a given AST node
    """

    def __init__(self, files: List[str]):
        self.files = files

    def infer_types(self, print_warnings=True):
        """
        Rewrite code to include inferred types

        Return dictionary with each variable in each method with what types it might be
        """

        # Run type inference analyzers
        analyzers = [_FunctionReturnInference]
        type_warnings = []
        for analyzer in analyzers:
            analyzer = analyzer()
            analyzer.check(self.files)
            type_warnings.extend(analyzer.report())

        if print_warnings:
            # Print warnings            
            for w in type_warnings:
                w.print_warning()

        # Return dictionary of warning
        return [w.__dict__ for w in type_warnings]


def get_test_files():
    # Get list of test files
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    test_file_dir = os.path.join(directory, '../test_files')
    test_files = []
    for f in os.listdir(test_file_dir):
        full_path = os.path.join(test_file_dir, f)
        test_files.append(os.path.relpath(full_path))
    return test_files


def test_type_inference():
    # Run type inference module on them
    type_inferrer = TypeInference(get_test_files())
    types = type_inferrer.infer_types()


def test_import_map():
    import_map = _MapImportTypes(get_test_files().pop())


if __name__ == '__main__':
    test_type_inference()
