import ast
import tokenize
import os

from scalpel.typeinfer.typeinfer import TypeInference

path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]


def parse_file(filename):
    with tokenize.open(filename) as f:
        return ast.parse(f.read(), filename=filename)


def get_func_def_at_lineno(ast_tree, lineno):
    candidate = None
    for item in ast.walk(ast_tree):
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if item.lineno == lineno:
                # Ignore whatever is after our line
                return item

    return None


def format_type_annot(annot):
    if isinstance(annot, ast.Tuple):
        # print(ast.dump(annot))
        return [format_type_annot(elt) for elt in annot.elts]
    if isinstance(annot, ast.Name):
        return annot.id
    if isinstance(annot, ast.Str):
        return annot.s

    elif isinstance(annot, ast.Constant):
        if annot.value is None:
            return "empty"
        return annot.value
    elif isinstance(annot, ast.Subscript):
        if isinstance(annot.value, ast.Name) and annot.value.id in ["Optional", "t.Optional"]:
            return "Any"
        if isinstance(annot.value, ast.Name) and annot.value.id in ["Union", "t.Union"]:
            return format_type_annot(annot.slice)

        if isinstance(annot.value, ast.Name) and annot.value.id == "Literal":
            return format_type_annot(annot.slice)

        return format_type_annot(annot.value)
    elif isinstance(annot, ast.Attribute):
        attr_name = get_attr_name(annot)
        return attr_name
    elif isinstance(annot, ast.Index):
        return format_type_annot(annot.value)
    elif isinstance(annot, ast.NameConstant):
        if annot.value is None:
            return "empty"
        else:
            return annot.value
    else:
        # return ast.dump(annot)
        # print(ast.dump(annot), 'testing')
        return ""


def get_attr_name(node):
    if isinstance(node, ast.Call):
        # to be test
        return get_attr_name(node.func)
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return get_attr_name(node.value) + "." + node.attr
    elif isinstance(node, ast.Subscript):
        return ""
    return ""  # other types


def test_pytest_case1():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case1.py'
    infferer = TypeInference(name='pytest_case1.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        #print(return_type_prediction)
        #print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()

    print(inferred)
    print(len(inferred))


def test_pytest_case2():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case2.py'
    infferer = TypeInference(name='pytest_case2.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case3():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case3.py'
    infferer = TypeInference(name='pytest_case3.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case4():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case4.py'
    infferer = TypeInference(name='pytest_case4.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case5():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case5.py'
    infferer = TypeInference(name='pytest_case5.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case6():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case6.py'
    infferer = TypeInference(name='pytest_case6.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case7():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case7.py'
    infferer = TypeInference(name='pytest_case7.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case8():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case8.py'
    infferer = TypeInference(name='pytest_case8.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case9():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case9.py'
    infferer = TypeInference(name='pytest_case9.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


def test_pytest_case10():
    entry_point = current_directory + '/test-cases/typeinfer_real_cases/pytest_case10.py'
    infferer = TypeInference(name='pytest_case10.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = list(return_type_prediction)[0]
        # print(return_type_prediction)
        # print(format_type_annot(func_def.returns).lower())
        assert return_type_prediction == format_type_annot(func_def.returns).lower()
    print(inferred)
    print(len(inferred))


if __name__ == "__main__":
    test_pytest_case1()
    test_pytest_case2()
    #test_pytest_case3()
    #test_pytest_case4()
    #test_pytest_case5()
