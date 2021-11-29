"""
This module contains a set of data classes.
"""
import ast
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class TypeWarning:
    """
    Holds information about a type warning
    """
    warning: str  # Stores warning text
    line: int  # Line number of warning
    file: str  # Line where the warning was found
    variable: str  # Name of the variable

    def print_warning(self):
        print(f"{self.file}:{self.line}: {self.warning}")


@dataclass
class ScalpelVariable:
    """
    Holds information about a variable
    """
    name: str  # The name of the variable
    function: str  # The name of the function where the variable is defined
    line: int  # The line number that the variable is defined at
    type: str = None  # The type of the variable as a string
    in_conditional: bool = False  # Whether the variable is involved in any conditional statements
    in_equality: bool = False  # Whether the variable is involved in an equality statement
    is_callable: bool = False  # Whether the variable has been called as a function
    called_methods: List[str] = None  # List of methods called from the variable
    binary_operation: ast.BinOp = None  # Binary operation assignment
    is_arg: bool = None  # Whether the variable is an argument in a function

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


@dataclass
class ProcessedFile:
    """
    Holds information about a processed file
    """
    type_dict: dict = field(default_factory=dict)
    type_gt: dict = field(default_factory=dict)
    type_stem_links: dict = field(default_factory=dict)
    node_type_comment: dict = field(default_factory=dict)
    static_assignments: list = field(default_factory=list)
    line_numbers: dict = field(default_factory=dict)
    imports: dict = field(default_factory=dict)
