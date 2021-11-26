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
        return annot.value
    else:
        # return ast.dump(annot)
        # print(ast.dump(annot), 'testing')
        return ""


def get_attr_name (node):
    if isinstance(node, ast.Call):
        # to be test
        return get_attr_name(node.func)
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return get_attr_name(node.value)+"."+node.attr
    elif isinstance(node, ast.Subscript):
        return ""
    return ""  # other types

def test_pytest_case1():
    entry_point = current_directory+'/test-cases/typeinfer_basecase/pytest_outcomes.py'
    infferer = TypeInference(name='pytest_outcomes.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast,return_info['line_number'])
        return_type_prediction = return_info['type']
        if len(return_type_prediction) == 1:
            return_type_prediction = return_type_prediction.pop()
        if next(iter(return_type_prediction)) == 'empty':
            assert format_type_annot(func_def.returns) == None
            continue
        assert return_type_prediction == format_type_annot(func_def.returns).lower()

    print(inferred)
    print(len(inferred))

def test_pytest_case2():
    entry_point = current_directory + '/test-cases/typeinfer_basecase/pytest_io_saferepr.py'
    infferer = TypeInference(name='pytest_io_saferepr.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    file_ast = parse_file(entry_point)
    for return_info in inferred:
        func_def = get_func_def_at_lineno(file_ast, return_info['line_number'])
        return_type_prediction = return_info['type']

        if next(iter(return_type_prediction)) == 'empty':
            assert format_type_annot(func_def.returns) == None
            continue
        print(return_type_prediction)
        print(format_type_annot(func_def.returns))
        assert format_type_annot(func_def.returns).lower() in return_type_prediction
    print(inferred)
    print(len(inferred))


'''
# Wrong Case
# function wcwidth() should return int type, instead of 'any'
def test_pytest_case3():
    entry_point = current_directory + '/test-cases/typeinfer_basecase/pytest_io_wcwidth.py'
    infferer = TypeInference(name='pytest_io_wcwidth.py',
                             entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    print(inferred)
    print(len(inferred))
'''


# Below are error cases


def test_pytest_case4():
    entry_point = current_directory + '/test-cases/typeinfer_basecase/pytest_io_terminalwriter.py'
    infferer = TypeInference(name='pytest_io_terminalwriter.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    print(inferred)
    print(len(inferred))

def test_pytest_case5():
    entry_point = current_directory + '/test-cases/typeinfer_basecase/pytest_unittest.py'
    infferer = TypeInference(name='pytest_unittest.py', entry_point=entry_point)
    infferer.infer_types()
    inferred = infferer.get_types()
    inferred = [item for item in inferred if 'parameter' not in item and 'variable' not in item]
    print(inferred)
    print(len(inferred))


if __name__ == "__main__":
    test_pytest_case1()
    test_pytest_case2()
    #test_pytest_case3()
    test_pytest_case4()
    test_pytest_case5()
