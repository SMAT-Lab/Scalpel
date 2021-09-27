"""
Tomas Bolger 2021
Python 3.9
Automated comparison of Scalpel Type inference output to PyType stub file
"""

import ast
import os
import typing
import tokenize
import astunparse
from pprint import pprint

from scalpel.typeinfer.analysers import ClassSplitVisitor
from scalpel.typeinfer.typeinfer import TypeInference


def get_stub_function_returns(stub_file_path):
    with tokenize.open(stub_file_path) as stub_file:
        stub_source = stub_file.read()
        tree = ast.parse(stub_source, mode='exec', type_comments=True)

        # Parse stub file code
        type_dict = {
            'functions': {}
        }
        unparsed = stub_source
        unparsed = unparsed.replace('nothing', 'None')  # Replace nothing with None
        module = ast.parse(unparsed, mode='exec')
        code = compile(module, filename=stub_file_path, mode='exec')
        namespace = {}
        while True:
            try:
                exec(code, namespace)
                break
            except NameError as e:
                # Remove name and reparse code
                name = str(e).split("'")[1]
                unparsed = unparsed.replace(f"({name})", '')
                module = ast.parse(unparsed, mode='exec')
                code = compile(module, filename=stub_file_path, mode='exec')
            except Exception as e:
                raise

        # Get function and method names
        all_methods, all_classes, import_nodes = get_nodes(tree)
        function_names = []
        for class_node in all_classes:
            class_name = class_node.name
            class_visitor = ClassSplitVisitor()
            class_visitor.visit(class_node)

            class_obj = namespace.get(class_name)

            for function_node in class_visitor.fun_nodes:
                function_name = function_node.name
                method_name = f"{class_name}.{function_name}"
                function_names.append(function_name)
                function_def = class_obj.__dict__[function_name]
                type_values = typing.get_type_hints(function_def)
                if 'typing' in str(type_values['return']):
                    type_dict['functions'][method_name] = str(type_values['return']).replace('typing.', '')
                else:
                    type_dict['functions'][method_name] = type_values['return'].__name__

        for function_node in all_methods:
            function_name = function_node.name
            function_names.append(function_node.name)
            type_values = typing.get_type_hints(namespace[function_name])
            if 'typing' in str(type_values['return']):
                type_dict['functions'][function_name] = str(type_values['return']).replace('typing.', '')
            else:
                type_dict['functions'][function_name] = type_values['return'].__name__

        return type_dict


def basecase_scalpel_vs_pytype():
    correct, total = 0, 0
    for i in range(1, 13):
        file_name = f'case{i}.py'
        print(file_name)
        pytype_stub_file = f'../basecase/basecase_pytype/pyi/{file_name}i'

        # Get PyType inferred types as dict
        inferred_pytype = get_stub_function_returns(pytype_stub_file)

        # Get scalpel inferred types
        inferrer = TypeInference(name=file_name, entry_point=f'../basecase/{file_name}')
        inferrer.infer_types()
        inferred_scalpel = inferrer.get_types()

        # Check PyType function returns
        scalpel_functions = {}
        for f in inferred_scalpel:
            if 'variable' not in f and 'parameter' not in f:
                scalpel_functions[f['function']] = f
        for function_name, pytype_return in inferred_pytype['functions'].items():
            if '__init__' in function_name:
                continue

            scalpel_function = scalpel_functions.get(function_name)
            if scalpel_function is not None:
                # TODO: Improve comparison step here
                # Compare types
                scalpel_return_set = scalpel_function.get('type')
                pytype_return_set = {pytype_return}
                print(scalpel_return_set, pytype_return_set)
                # Perform check
                if scalpel_return_set == pytype_return_set:
                    correct += 1
                elif len(scalpel_return_set) == len(pytype_return_set):
                    # Check first element lowercase
                    scalpel_return = next(iter(scalpel_return_set))
                    pytype_return = next(iter(pytype_return_set))
                    if scalpel_return.lower() in pytype_return.lower():
                        correct += 1
                elif len(pytype_return_set) == 1:
                    pytype_return = next(iter(pytype_return_set))
                    if 'Union' in pytype_return:
                        scalpel_union = 'Union['
                        for index, s in enumerate(scalpel_return_set):
                            if index + 1 != len(scalpel_return_set):
                                scalpel_union += s + ', '
                            else:
                                scalpel_union += s + ']'
                        if scalpel_union == pytype_return:
                            correct += 1
                # Increment total
                total += 1

    return total, correct


def get_nodes(tree):
    fun_nodes = []
    class_nodes = []
    import_nodes = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            fun_nodes += [node]
        if isinstance(node, ast.ClassDef):
            class_nodes += [node]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            import_nodes += [node]

    return fun_nodes, class_nodes, import_nodes


if __name__ == '__main__':
    total, correct = basecase_scalpel_vs_pytype()
    print(f"Total: {total}\nCorrect: {correct}")
