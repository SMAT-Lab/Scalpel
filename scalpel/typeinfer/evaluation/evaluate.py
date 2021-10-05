"""
Tomas Bolger 2021
Python 3.9
Automated comparison of Scalpel Type inference output to PyType stub file
"""

import ast
import os
import typing
import tokenize
from pprint import pprint
from typed_ast import ast3

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
                # print(scalpel_return_set, pytype_return_set)
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


def evaluate_repos():
    # Run Scalpel type inference on each repository in the repos folder
    repo_list = os.listdir('pytype_stubs')
    repo_list = ['deezer__spleeter']#'minimaxir__big-list-of-naughty-strings']#, 'openai__gym', 'psf__requests', , 'psf__black']
    for repo in repo_list:
        # Get file paths
        print(repo)
        path_dict = get_file_paths(repo)

        # Get scalpel inferred types
        inferrer = TypeInference(name=repo, entry_point=f'source_repos/{repo}')
        inferrer.infer_types()
        scalpel_inferred = inferrer.get_types()

        # Get PyType inferred types from stub files
        pytype_inferred = []
        for file in path_dict.keys():
            pytype_inferred.extend(get_stub_types(file))

        compare_dict = {}
        pytype_total = 0
        for inferred in pytype_inferred:
            file, function, p_type = inferred['file'], inferred['function'], inferred['type']
            file = file.replace('.pyi', '.py')  # Replace file extension so we can compare to the same file name
            if compare_dict.get(file):
                compare_dict[file][function] = p_type
            else:
                compare_dict[file] = {function: p_type}

            if p_type is not None:
                # Only incrementing total if return type is not None,
                # since our module doesn't report None for functions with no return
                pytype_total += 1  # Increment PyType inferred total count

        # Compare with Scalpel
        scalpel_total = 0
        for inferred in scalpel_inferred:
            if 'variable' not in inferred and 'parameter' not in inferred:
                file, function, s_type = inferred['file'], inferred['function'], inferred['type']

                if file_types := compare_dict.get(file):
                    if p_type := file_types.get(function):
                        print(file, function, p_type, s_type)
                        if len(s_type) == 1:
                            s_type = next(iter(s_type))
                            if str(p_type).lower() in str(s_type).lower():
                                print('adding')
                                scalpel_total += 1
        try:
            print(f'Repository: {repo}, Accuracy: {round(scalpel_total / pytype_total, 4) * 100}%')
        except ZeroDivisionError:
            print(f'Repository: {repo}, Accuracy: 100%')


def get_stub_types(stub_file_path: str):
    file_name = stub_file_path.split('/')[-1]
    with open(stub_file_path, 'r') as stub_file:
        source = stub_file.read()
        try:
            tree = ast3.parse(source, mode='exec')
        except Exception as e:
            # print(e)
            pass

        inferred_types = []

        for node in ast3.walk(tree):
            if isinstance(node, ast3.FunctionDef):
                function_name = node.name

                # Function return
                return_node = node.returns
                if isinstance(return_node, ast3.Subscript):
                    return_type = return_node.value.id
                elif isinstance(return_node, ast3.NameConstant):
                    return_type = return_node.value
                elif isinstance(return_node, ast3.Name):
                    return_type = return_node.id
                elif isinstance(return_node, ast3.Attribute):
                    return_type = return_node.attr
                else:
                    raise Exception(f'Return node type not accounted for: {type(return_node)}')
                inferred_types.append({
                    'file': file_name,
                    'function': function_name,
                    'type': return_type
                })

                # Function parameters
                for argument in node.args.args:
                    # print(function_name, argument.arg, argument.type_comment)
                    pass

    return inferred_types


def get_file_paths(repo_name: str):
    # Get PyType stub files
    path_dict = {}
    for root, subdirs, files in os.walk(f'pytype_stubs/{repo_name}/pyi'):
        for file_name in files:
            if file_name.endswith('.pyi'):
                pyi_path = f'{root}/{file_name}'
                scalpel_path = pyi_path.replace('/pyi/', '/')
                path_dict[pyi_path] = scalpel_path
    return path_dict


if __name__ == '__main__':
    # total, correct = basecase_scalpel_vs_pytype()
    # print(f"Total: {total}\nCorrect: {correct}")
    evaluate_repos()
    # get_file_paths('psf__black')
