import sys

py_version_above_38 = True
if sys.version_info >= (3, 8):
    py_version_above_38 = True
elif sys.version_info >= (3, 5) and sys.version_info < (3, 8):
    py_version_above_38 = False
else:
    raise Exception("Must use Python 3.5+ ")


def actual_data_case_1():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case1.py",
                    "line_number": 10,
                    "function": "my_function",
                    "type": {"Dict[str, str]"},
                },
                {
                    "file": "case1.py",
                    "line_number": 14,
                    "variable": "my_var",
                    "function": "my_function",
                    "type": {"Dict[str, str]"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case1.py",
                    "line_number": 10,
                    "function": "my_function",
                    "type": {"Dict[any, any]"},
                },
                {
                    "file": "case1.py",
                    "line_number": 14,
                    "variable": "my_var",
                    "function": "my_function",
                    "type": {"Dict[any, any]"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_2():
    actual_data = sorted(
        [
            {
                "file": "case2.py",
                "line_number": 6,
                "function": "my_function",
                "type": {"str"},
            }
        ],
        key=lambda x: str(x),
    )

    return actual_data


def actual_data_case_3():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case3.py",
                    "line_number": 8,
                    "function": "my_function",
                    "type": {"str", "int"},
                },
                {
                    "file": "case3.py",
                    "line_number": 8,
                    "parameter": "my_bool",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case3.py",
                    "line_number": 10,
                    "variable": "my_int",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case3.py",
                    "line_number": 13,
                    "variable": "my_str",
                    "function": "my_function",
                    "type": {"str"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case3.py",
                    "line_number": 8,
                    "function": "my_function",
                    "type": {"str", "int"},
                },
                {
                    "file": "case3.py",
                    "line_number": 8,
                    "parameter": "my_bool",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case3.py",
                    "line_number": 10,
                    "variable": "my_int",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case3.py",
                    "line_number": 13,
                    "variable": "my_str",
                    "function": "my_function",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_4():
    actual_data = sorted(
        [
            {
                "file": "case4.py",
                "line_number": 12,
                "function": "MyClass.get_hash",
                "type": {"Dict[any, any]"},
            }
        ],
        key=lambda x: str(x),
    )

    return actual_data


def actual_data_case_5():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case5.py",
                    "line_number": 9,
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case5.py",
                    "line_number": 10,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case5.py",
                    "line_number": 11,
                    "variable": "y",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case5.py",
                    "line_number": 12,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"int"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case5.py",
                    "line_number": 9,
                    "function": "my_function",
                    "type": {None},
                },
                {
                    "file": "case5.py",
                    "line_number": 10,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case5.py",
                    "line_number": 11,
                    "variable": "y",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case5.py",
                    "line_number": 12,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_6():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case6.py",
                    "line_number": 9,
                    "function": "my_function",
                    "type": {"str"},
                },
                {
                    "file": "case6.py",
                    "line_number": 10,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case6.py",
                    "line_number": 11,
                    "variable": "y",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case6.py",
                    "line_number": 12,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"int"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case6.py",
                    "line_number": 9,
                    "function": "my_function",
                    "type": {"str"},
                },
                {
                    "file": "case6.py",
                    "line_number": 10,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case6.py",
                    "line_number": 11,
                    "variable": "y",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case6.py",
                    "line_number": 12,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_7():
    actual_data = sorted(
        [
            {
                "file": "case7.py",
                "line_number": 8,
                "variable": "_",
                "function": "my_function",
                "type": {"int"},
            },
        ],
        key=lambda x: str(x),
    )
    return actual_data


def actual_data_case_8():
    actual_data = sorted(
        [
            {
                "file": "case8.py",
                "line_number": 7,
                "function": "my_function",
                "type": {"callable"},
            },
            {
                "file": "case8.py",
                "line_number": 8,
                "function": "my_inner_function",
                "type": {"int"},
            },
        ],
        key=lambda x: str(x),
    )

    return actual_data


def actual_data_case_9():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case9.py",
                    "line_number": 13,
                    "function": "ParentClass.my_function",
                    "type": {"List[int]"},
                },
                {
                    "file": "case9.py",
                    "line_number": 21,
                    "function": "ChildClass.my_function",
                    "type": {"List[int]"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case9.py",
                    "line_number": 13,
                    "function": "ParentClass.my_function",
                    "type": {"List[None]"},
                },
                {
                    "file": "case9.py",
                    "line_number": 21,
                    "function": "ChildClass.my_function",
                    "type": {"List[None]"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_10():
    actual_data = sorted(
        [
            {
                "file": "case10.py",
                "line_number": 10,
                "function": "my_function",
                "type": {"defaultdict"},
            },
            {
                "file": "case10.py",
                "line_number": 11,
                "variable": "my_default_dict",
                "function": "my_function",
                "type": {"defaultdict"},
            },
        ],
        key=lambda x: str(x),
    )

    return actual_data


def actual_data_case_11():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case11.py",
                    "line_number": 7,
                    "function": "my_function",
                    "type": {"int", "str"},
                },
                {
                    "file": "case11.py",
                    "line_number": 7,
                    "parameter": "my_bool",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case11.py",
                    "line_number": 9,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case11.py",
                    "line_number": 11,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"str"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case11.py",
                    "line_number": 7,
                    "function": "my_function",
                    "type": {"int", "str"},
                },
                {
                    "file": "case11.py",
                    "line_number": 7,
                    "parameter": "my_bool",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case11.py",
                    "line_number": 9,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case11.py",
                    "line_number": 11,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_12():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case12.py",
                    "line_number": 12,
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case12.py",
                    "line_number": 12,
                    "parameter": "my_val",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case12.py",
                    "line_number": 13,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case12.py",
                    "line_number": 14,
                    "variable": "y",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case12.py",
                    "line_number": 15,
                    "variable": "g",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case12.py",
                    "line_number": 16,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"int"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case12.py",
                    "line_number": 12,
                    "function": "my_function",
                    "type": {None},
                },
                {
                    "file": "case12.py",
                    "line_number": 12,
                    "parameter": "my_val",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case12.py",
                    "line_number": 13,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case12.py",
                    "line_number": 14,
                    "variable": "y",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case12.py",
                    "line_number": 15,
                    "variable": "g",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case12.py",
                    "line_number": 16,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_13():
    actual_data = sorted(
        [
            {
                "file": "case13.py",
                "line_number": 8,
                "function": "first_function",
                "type": {"str"},
            },
            {
                "file": "case13.py",
                "line_number": 12,
                "function": "second_function",
                "type": {"str"},
            },
            {
                "file": "case13.py",
                "line_number": 16,
                "function": "third_function",
                "type": {"str"},
            },
        ],
        key=lambda x: str(x),
    )

    return actual_data


def actual_data_case_14():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case14.py",
                    "line_number": 8,
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case14.py",
                    "line_number": 9,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"int"},
                },
                {
                    "file": "case14.py",
                    "line_number": 10,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"int"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case14.py",
                    "line_number": 8,
                    "function": "my_function",
                    "type": {None},
                },
                {
                    "file": "case14.py",
                    "line_number": 9,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case14.py",
                    "line_number": 10,
                    "variable": "z",
                    "function": "my_function",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_15():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case15.py",
                    "line_number": 11,
                    "function": "my_function",
                    "type": {"str"},
                },
                {
                    "file": "case15.py",
                    "line_number": 12,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"str"},
                },
                {
                    "file": "case15.py",
                    "line_number": 8,
                    "function": "getcwd",
                    "type": {"str"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case15.py",
                    "line_number": 11,
                    "function": "my_function",
                    "type": {None},
                },
                {
                    "file": "case15.py",
                    "line_number": 12,
                    "variable": "x",
                    "function": "my_function",
                    "type": {"any"},
                },
                {
                    "file": "case15.py",
                    "line_number": 8,
                    "function": "getcwd",
                    "type": {"str"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_16():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "file1.py",
                    "line_number": 7,
                    "function": "class_method",
                    "type": {"Tuple[str]"},
                },
                {
                    "file": "file1.py",
                    "line_number": 7,
                    "function": "MyClass.class_method",
                    "type": {"Tuple[str]"},
                },
                {
                    "file": "file2.py",
                    "line_number": 1,
                    "function": "imported_function",
                    "type": {"Tuple[str]"},
                },
                {
                    "file": "file2.py",
                    "line_number": 2,
                    "variable": "return_value",
                    "function": "imported_function",
                    "type": {"Tuple[str]"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "file1.py",
                    "line_number": 6,
                    "function": "class_method",
                    "type": {"Tuple[str]"},
                },
                {
                    "file": "file1.py",
                    "line_number": 6,
                    "function": "MyClass.class_method",
                    "type": {"Tuple[str]"},
                },
                {
                    "file": "file2.py",
                    "line_number": 1,
                    "function": "imported_function",
                    "type": {"Tuple[str]"},
                },
                {
                    "file": "file2.py",
                    "line_number": 2,
                    "variable": "return_value",
                    "function": "imported_function",
                    "type": {"Tuple[str]"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_17():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case17.py",
                    "line_number": 1,
                    "function": "fun1",
                    "type": {"float"},
                },
                {
                    "file": "case17.py",
                    "line_number": 5,
                    "function": "fun2",
                    "type": {"float"},
                },
                {
                    "file": "case17.py",
                    "line_number": 1,
                    "parameter": "a",
                    "function": "fun1",
                    "type": {"float"},
                },
                {
                    "file": "case17.py",
                    "line_number": 5,
                    "parameter": "a",
                    "function": "fun2",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )
    else:
        actual_data = sorted(
            [
                {
                    "file": "case17.py",
                    "line_number": 1,
                    "function": "fun1",
                    "type": {"any"},
                },
                {
                    "file": "case17.py",
                    "line_number": 5,
                    "function": "fun2",
                    "type": {None},
                },
                {
                    "file": "case17.py",
                    "line_number": 1,
                    "parameter": "a",
                    "function": "fun1",
                    "type": {"any"},
                },
                {
                    "file": "case17.py",
                    "line_number": 5,
                    "parameter": "a",
                    "function": "fun2",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_18():
    actual_data = sorted(
        [
            {
                "file": "case18.py",
                "line_number": 5,
                "function": "MyParentClass.my_function",
                "type": {"str"},
            },
            {
                "file": "case18.py",
                "line_number": 11,
                "function": "ChildClass.my_function",
                "type": {"List[str]"},
            },
        ],
        key=lambda x: str(x),
    )

    return actual_data


def actual_data_case_19():
    pass


def actual_data_case_20():
    if py_version_above_38:
        actual_data = sorted(
            [
                {
                    "file": "case20.py",
                    "line_number": 1,
                    "function": "add",
                    "type": {"int", "str"},
                },
                {
                    "file": "case20.py",
                    "line_number": 1,
                    "parameter": "x",
                    "function": "add",
                    "type": {"int", "str"},
                },
                {
                    "file": "case20.py",
                    "line_number": 1,
                    "parameter": "y",
                    "function": "add",
                    "type": {"int", "str"},
                },
            ],
            key=lambda x: str(x),
        )

    else:
        actual_data = sorted(
            [
                {
                    "file": "case20.py",
                    "line_number": 1,
                    "function": "add",
                    "type": {None},
                },
                {
                    "file": "case20.py",
                    "line_number": 1,
                    "parameter": "x",
                    "function": "add",
                    "type": {"any"},
                },
                {
                    "file": "case20.py",
                    "line_number": 1,
                    "parameter": "y",
                    "function": "add",
                    "type": {"any"},
                },
            ],
            key=lambda x: str(x),
        )

    return actual_data


def actual_data_case_23():
    actual_data = sorted(
        [
            {
                "file": "case23.py",
                "line_number": 1,
                "function": "my_function",
                "type": {"int", "str"},
            },
            {
                "file": "case23.py",
                "line_number": 1,
                "parameter": "x",
                "function": "my_function",
                "type": {"any"},
            },
        ],
        key=lambda x: str(x),
    )

    return actual_data


def actual_data_case_24():
    actual_data = sorted(
        [
            {
                "file": "case24.py",
                "line_number": 1,
                "function": "my_function",
                "type": {"any"},
            },
            {
                "file": "case24.py",
                "line_number": 1,
                "parameter": "x",
                "function": "my_function",
                "type": {"callable"},
            },
            {
                "file": "case24.py",
                "line_number": 2,
                "variable": "y",
                "function": "my_function",
                "type": {"any"},
            },
        ],
        key=lambda x: str(x),
    )

    return actual_data
