"""
Tomas Bolger 2021
Python 3.9
Automated comparison of Scalpel Type inference output to PyType stub file
"""
import multiprocessing
import ast
import os
import typing
import tokenize
import pandas
from pprint import pprint
from typed_ast import ast3

from scalpel.typeinfer.analysers import ClassSplitVisitor
from scalpel.typeinfer.typeinfer import TypeInference

dirname = os.path.dirname(__file__)


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


def do_evaluate_repo(repo):
    print(repo)
    filename = f"{repo}.xlsx"

    output_data = []
    # Get file paths
    path_dict = get_file_paths(repo)

    # Get scalpel inferred types
    # inferrer = TypeInference(name=repo, entry_point=f'source_repos/{repo}')
    if repo in ["beurtschipper__Depix", "deezer__spleeter", "facebookresearch__Detectron", "psf__black", "psf__requests"]:
        repo_folder = "main_repos"
    else:
        repo_folder = "source_repos"
    inferrer = TypeInference(name=repo, entry_point=os.path.join(dirname, repo_folder, repo))
    inferrer.infer_types()
    scalpel_inferred = inferrer.get_types()

    # Get PyType inferred types from stub files
    pytype_inferred = []
    for file in path_dict.keys():
        pytype_inferred.extend(get_stub_types(file))

    output_dict = {}
    compare_dict = {}
    pytype_total = 0
    for inferred in pytype_inferred:
        file, function, p_type = inferred['file'], inferred['function'], inferred['type']
        parameter = inferred.get('parameter')

        file = file.replace('.pyi', '.py')  # Replace file extension so we can compare to the same file name

        if parameter is None:
            # Function return
            if p_type is not None:
                # Only including in total if return type is not None,
                # since our module doesn't report None for functions with no return
                if compare_dict.get(file):
                    compare_dict[file][function] = {'return': p_type}
                else:
                    compare_dict[file] = {function: {'return': p_type}}
                pytype_total += 1  # Increment PyType inferred total count
            else:
                pass
        else:
            if file_ref := compare_dict.get(file):
                if file_ref.get(function):
                    compare_dict[file][function][parameter] = p_type
                else:
                    compare_dict[file][function] = {parameter: p_type}
            else:
                compare_dict[file] = {function: {parameter: p_type}}
            pytype_total += 1  # No need to check for None since PyType gives None for no argument type

        if file not in output_dict:
            output_dict[file] = {}
        if function not in output_dict[file]:
            output_dict[file][function] = {}
        output_dict[file][function]["p_type"] = p_type if p_type else "Any"
        # output_data.append([repo, file, function, p_type, ""])

    # Compare with Scalpel
    scalpel_total = 0
    for inferred in scalpel_inferred:
        if 'variable' not in inferred:
            file, function, s_type = inferred['file'], inferred['function'], inferred['type']
            parameter = inferred.get('parameter')

            # print(file, function, s_type, parameter)
            if file_types := compare_dict.get(file):
                if parameter is None:
                    # Function/method returns

                    # Check to see if we have a class method name from Scalpel
                    split_name = function.split('.')
                    if len(split_name) == 2:
                        function = split_name[1]

                    if p_function := file_types.get(function):
                        if p_type := p_function.get('return'):

                            output_data.append([repo, file, function, p_type if p_type else "Any", s_type])
                            # loop through the s_type set and check if any of the p_types equal the s_type and then
                            # add and continue

                            s_type = next(iter(s_type))
                            # check if s_type is a set
                            output_data.append([repo, file, function, p_type if p_type else "Any", s_type])
                            if s_type is not None and len(s_type) == 1:
                                s_type = next(iter(s_type))
                                if str(p_type).lower() in str(s_type).lower():
                                    scalpel_total += 1
                                    del p_function['return']  # Remove from dict
                                    continue

                else:
                    # Parameter type
                    if p_function := file_types.get(function):
                        # Check for named type
                        if p_type := p_function.get(parameter):
                            output_data.append([repo, file, function, p_type if p_type else "Any", s_type])
                            if len(s_type) == 1:
                                s_type = next(iter(s_type))
                                if str(p_type).lower() in str(s_type).lower():
                                    scalpel_total += 1
                                    del p_function[parameter]
                                    continue
                        else:
                            output_data.append([repo, file, function, p_type if p_type else "Any", s_type])
                            # PyType couldn't infer the return type, check to see if Scalpel returned 'any'
                            if s_type == 'any' and parameter in p_function.keys():
                                scalpel_total += 1
                                del p_function[parameter]
                                continue

    # Cleanup NoReturn (these are just functions with no return statement, Scalpel doesn't bother outputting this)
    for file in compare_dict.keys():
        for function in compare_dict[file].keys():
            if r_type := compare_dict[file][function].get('return'):
                if r_type == 'NoReturn' or r_type is None:
                    scalpel_total += 1
                    del compare_dict[file][function]['return']

    # output_data = []
    for repo_file_name, function_file in output_dict.items():
        for function_name, function in function_file.items():
            p_type = function["p_type"] if "p_type" in function else ""
            s_type = function["s_type"] if "s_type" in function else ""
            # output_data.append([repo, repo_file_name, function, p_type, s_type])

    pprint(compare_dict)
    try:
        print(f'PyType Total: {pytype_total}, Scalpel Total: {scalpel_total}')
        print(f'Repository: {repo}, Accuracy: {round(scalpel_total / pytype_total, 4) * 100}%')
        # find wins using comparisons between s_type and p_type and append to excel sheet
        spreadsheet_headers = ["Repository", "File Name", "Function Name", "PyType Type", "Scalpel Type"]
        df = pandas.DataFrame(output_data, columns=spreadsheet_headers)
        parse_dataframe_status(df, filename)

    except ZeroDivisionError:
        print(f'Repository: {repo}, Accuracy: 100%')

    print(f"Finished analysing {repo}")


def parse_dataframe_status(df, filename):
    """
    Parses a dataframe to calculate how many wins/losses we achieved
    """

    new_data = []
    wins = 0
    losses = 0
    neutrals = 0
    for item in df.iloc:
        s_type = item["Scalpel Type"]
        p_type = item["PyType Type"]
        if p_type == None:
            p_type = "Any"

        if isinstance(s_type, set):

            s_type = [x if x is not None else "any" for x in s_type]

            if "any" in p_type.lower() and not all(["any" in x.lower() for x in s_type]):
                win_status = "Win"
                wins += 1
            elif any([x.lower() in p_type.lower() or p_type.lower() in x.lower() for x in s_type]):
                win_status = "Neutral"
                neutrals += 1
            else:
                # probs lost here
                # "any" in p_type and not all([x.lower() == "any" for x in s_type])
                win_status = "Loss"
                losses += 1
        else:
            s_type = "any" if s_type is None else s_type
            if p_type.lower() in s_type.lower() or s_type.lower() in p_type.lower():
                win_status = "Neutral"
                neutrals += 1
            elif "any" in p_type.lower() and "any" not in s_type.lower():
                win_status = "Win"
                wins += 1
            else:
                win_status = "Loss"
                losses += 1
        new_line = list(item.values) + [win_status]
        new_data.append(new_line)

    columns = list(df.columns) + ["Status"]
    total_checks = wins + neutrals + losses
    new_data.append([f'Total comparisons:', wins + neutrals + losses, 'PyType Wins:', losses, "Scalpel Wins:", wins])
    new_data.append([""] * (len(columns) - 2) + ["Scalpel Accuracy:", round((total_checks - losses)/total_checks if total_checks else 1, 4) * 100])
    # Divide by 1 if we have
    new_data.append(
        [""] * (len(columns) - 2) + ["Accuracy vs PyType", round(wins / losses if losses else 1, 4) * 100])

    new_df = pandas.DataFrame(new_data, columns=columns)
    styled_df = new_df.style.applymap(colouring)

    styled_df.to_excel(os.path.join(dirname, "evaluation_outputs", filename), index=False)
    return new_df


# code taken from https://stackoverflow.com/questions/43839112/format-the-color-of-a-cell-in-a-pandas-dataframe-according-to-multiple-condition/43839318 # noqa
def colouring(val):
    if val == "Win":
        color = 'green'
    elif val == "Neutral":
        color = 'orange'
    elif val == "Loss":
        color = 'red'
    else:
        color = "white"
    return f'background-color: {color}'


def evaluate_repos():
    # Run Scalpel type inference on each repository in the repos folder
    repo_list = os.listdir('pytype_stubs')
    # repo_list = ['psf__requests', 'deezer__spleeter', 'minimaxir__big-list-of-naughty-strings', 'openai__gym', 'psf__requests', 'psf__black']
    repo_list = ['docker__compose', 'pallets__flask', 'drduh__macOS-Security-and-Privacy-Guide',
                 'eriklindernoren__ML-From-Scratch', 'tqdm__tqdm', 'deezer__spleeter', 'wangzheng0822__algo',
                 'luong-komorebi__Awesome-Linux-Software', 'josephmisiti__awesome-machine-learning',
                 'beurtschipper__Depix', 'nvbn__thefuck', 'soimort__you-get', '521xueweihan__HelloGitHub',
                 'tornadoweb__tornado', 'psf__black', 'sebastianruder__NLP-progress', 'keon__algorithms',
                 'chubin__cheat.sh', 'faif__python-patterns', 'minimaxir__big-list-of-naughty-strings',
                 'donnemartin__interactive-coding-challenges', 'httpie__httpie', 'shadowsocks__shadowsocks',
                 'floodsung__Deep-Learning-Papers-Reading-Roadmap', 'littlecodersh__ItChat', 'locustio__locust',
                 'openai__gym', 'python-telegram-bot__python-telegram-bot', 'vinta__awesome-python',
                 'google-research__bert', 'public-apis__public-apis', 'facebookresearch__detectron2',
                 'trailofbits__algo', 'swisskyrepo__PayloadsAllTheThings', 'google__python-fire',
                 '0voice__interview_internal_reference', 'facebookresearch__Detectron', 'satwikkansal__wtfpython',
                 'sherlock-project__sherlock', 'psf__requests']
    # repo_list = ["beurtschipper__Depix", "deezer__spleeter", "facebookresearch__Detectron", "psf__black", "psf__requests", ]
    # repo_list = ['beurtschipper__Depix']
    all_threads = []
    for repo in repo_list:
        # do_evaluate_repo(repo)  # run this if you want it done without multithreading

        # Multithreading doesn't work due to the changing of current working dirs/pwd
        # So we're using multiprocessing
        thread = multiprocessing.Process(target=do_evaluate_repo, args=[repo])
        thread.start()
        all_threads.append(thread)

    for thread in all_threads:
        thread.join()


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
                decorator_names = [d.id for d in node.decorator_list if isinstance(d, ast3.Name)]
                if 'overload' not in decorator_names:
                    function_name = node.name
                    # Function return
                    return_node = node.returns
                    return_type = None
                    if isinstance(return_node, ast3.Subscript):
                        if isinstance(return_node.value, ast3.Name):
                            return_type = return_node.value.id
                    elif isinstance(return_node, ast3.NameConstant):
                        return_type = return_node.value
                    elif isinstance(return_node, ast3.Name):
                        return_type = return_node.id
                    elif isinstance(return_node, ast3.Attribute):
                        return_type = return_node.attr
                    else:
                        raise Exception(f'Return node type not accounted for: {type(return_node)}')

                    if return_type is not None:
                        inferred_types.append({
                            'file': file_name,
                            'function': function_name,
                            'type': return_type
                        })

                    # Function parameters
                    for argument in node.args.args:
                        if argument.arg != 'self':
                            inferred_types.append({
                                'file': file_name,
                                'function': function_name,
                                'parameter': argument.arg,
                                'type': argument.type_comment
                            })

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
