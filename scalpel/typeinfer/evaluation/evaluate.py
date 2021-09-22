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

from scalpel.typeinfer.typeinfer import TypeInference


def get_stub_function_returns(stub_file_path):
    with tokenize.open(stub_file_path) as stub_file:
        stub_source = stub_file.read()
        tree = ast.parse(stub_source, mode='exec', type_comments=True)
        import_code = ""
        type_dict = {
            'functions': {}
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                import_code += astunparse.unparse(node)
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                unparsed = astunparse.unparse(node)
                unparsed = import_code + unparsed  # Add imports to function definition
                unparsed = unparsed.replace('nothing', 'None')  # Replace nothing with None
                module = ast.parse(unparsed, mode='exec')
                code = compile(module, filename=stub_file_path, mode='exec')
                namespace = {}
                exec(code, namespace)
                type_values = typing.get_type_hints(namespace[function_name])
                type_dict['functions'][function_name] = str(type_values['return']).replace('typing.', '')
        return type_dict


def basecase_scalpel_vs_pytype():
    get_stub_function_returns('../basecase/basecase_pytype/pyi/case1.pyi')
    basecase_files = [f for f in os.listdir('../basecase') if f.endswith('.py')]
    basecase_files = sorted(basecase_files)
    correct, total = 0, 0
    for i in range(1, 10):
        file_name = f'case{i}.py'
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
            if function_name == '__init__':
                continue
                
            scalpel_function = scalpel_functions[function_name]

            # Compare types
            scalpel_return_set = scalpel_function.get('type')
            pytype_return_set = {pytype_return}

            # Perform check
            if scalpel_return_set == pytype_return_set:
                correct += 1

            # Increment total
            total += 1

    return total, correct


if __name__ == '__main__':
    basecase_scalpel_vs_pytype()
