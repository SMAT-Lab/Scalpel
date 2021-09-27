"""
Tomas Bolger 2021
Python 3.9
Unittests for base cases
"""

import unittest

from typeinfer import TypeInference


class BaseCaseTests(unittest.TestCase):

    def test_case_1(self):
        infferer = TypeInference(name='case1.py', entry_point='basecase/case1.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case1.py', 'line_number': 10, 'function': 'my_function', 'type': {'Dict[str, str]'}},
             {'file': 'case1.py', 'line_number': 14, 'variable': 'my_var', 'function': 'my_function',
              'type': 'Dict[str, str]'}]
        )

    def test_case_2(self):
        infferer = TypeInference(name='case2.py', entry_point='basecase/case2.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case2.py', 'line_number': 6, 'function': 'my_function', 'type': {'str'}}]
        )

    def test_case_3(self):
        infferer = TypeInference(name='case3.py', entry_point='basecase/case3.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case3.py', 'line_number': 8, 'function': 'my_function', 'type': {'str', 'int'}},
             {'file': 'case3.py', 'line_number': 8, 'parameter': 'my_bool', 'function': 'my_function', 'type': 'any'},
             {'file': 'case3.py', 'line_number': 10, 'variable': 'my_int', 'function': 'my_function', 'type': 'int'},
             {'file': 'case3.py', 'line_number': 13, 'variable': 'my_str', 'function': 'my_function', 'type': 'str'}]
        )

    def test_case_4(self):
        infferer = TypeInference(name='case4.py', entry_point='basecase/case4.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case4.py', 'line_number': 12, 'function': 'MyClass.get_hash', 'type': {'Dict[any, any]'}}]
        )

    def test_case_5(self):
        infferer = TypeInference(name='case5.py', entry_point='basecase/case5.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case5.py', 'line_number': 9, 'function': 'my_function', 'type': {'int'}},
             {'file': 'case5.py', 'line_number': 10, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case5.py', 'line_number': 11, 'variable': 'y', 'function': 'my_function', 'type': 'int'},
             {'file': 'case5.py', 'line_number': 12, 'variable': 'z', 'function': 'my_function', 'type': 'int'}]
        )

    def test_case_6(self):
        infferer = TypeInference(name='case6.py', entry_point='basecase/case6.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case6.py', 'line_number': 9, 'function': 'my_function', 'type': {'str'}},
             {'file': 'case6.py', 'line_number': 10, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case6.py', 'line_number': 11, 'variable': 'y', 'function': 'my_function', 'type': 'int'},
             {'file': 'case6.py', 'line_number': 12, 'variable': 'z', 'function': 'my_function', 'type': 'int'}]
        )

    def test_case_7(self):
        infferer = TypeInference(name='case7.py', entry_point='basecase/case7.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            []
        )

    def test_case_8(self):
        infferer = TypeInference(name='case8.py', entry_point='basecase/case8.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case8.py', 'line_number': 7, 'function': 'my_function', 'type': {'callable'}},
             {'file': 'case8.py', 'line_number': 8, 'function': 'my_inner_function', 'type': {'int'}}]
        )

    def test_case_9(self):
        infferer = TypeInference(name='case9.py', entry_point='basecase/case9.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case9.py', 'line_number': 13, 'function': 'ParentClass.my_function', 'type': {'List[int]'}},
             {'file': 'case9.py', 'line_number': 21, 'function': 'ChildClass.my_function', 'type': {'List[int]'}}]
        )

    def test_case_10(self):
        infferer = TypeInference(name='case10.py', entry_point='basecase/case10.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case10.py', 'line_number': 10, 'function': 'my_function', 'type': {'defaultdict'}},
             {'file': 'case10.py', 'line_number': 11, 'variable': 'my_default_dict', 'function': 'my_function',
              'type': 'defaultdict'}]
        )

    def test_case_11(self):
        infferer = TypeInference(name='case11.py', entry_point='basecase/case11.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case11.py', 'line_number': 7, 'function': 'my_function', 'type': {'int', 'str'}},
             {'file': 'case11.py', 'line_number': 7, 'parameter': 'my_bool', 'function': 'my_function', 'type': 'any'},
             {'file': 'case11.py', 'line_number': 9, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case11.py', 'line_number': 11, 'variable': 'x', 'function': 'my_function', 'type': 'str'}]
        )

    def test_case_12(self):
        infferer = TypeInference(name='case12.py', entry_point='basecase/case12.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case12.py', 'line_number': 12, 'function': 'my_function', 'type': {'int'}},
             {'file': 'case12.py', 'line_number': 12, 'parameter': 'my_val', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 13, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 14, 'variable': 'y', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 15, 'variable': 'g', 'function': 'my_function', 'type': 'int'},
             {'file': 'case12.py', 'line_number': 16, 'variable': 'z', 'function': 'my_function', 'type': 'int'}]
        )

    def test_case_13(self):
        infferer = TypeInference(name='case13.py', entry_point='basecase/case13.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case13.py', 'line_number': 8, 'function': 'first_function', 'type': {'str'}},
             {'file': 'case13.py', 'line_number': 12, 'function': 'second_function', 'type': {'str'}},
             {'file': 'case13.py', 'line_number': 16, 'function': 'third_function', 'type': {'str'}}]
        )

    def test_case_14(self):
        infferer = TypeInference(name='case14.py', entry_point='basecase/case14.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case14.py', 'line_number': 8, 'function': 'my_function', 'type': {'int'}},
             {'file': 'case14.py', 'line_number': 9, 'variable': 'x', 'function': 'my_function', 'type': 'int'},
             {'file': 'case14.py', 'line_number': 10, 'variable': 'z', 'function': 'my_function', 'type': 'int'}]
        )

    def test_case_15(self):
        infferer = TypeInference(name='case15.py', entry_point='basecase/case15.py')
        infferer.infer_types()
        inferred = infferer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case15.py', 'line_number': 11, 'function': 'my_function', 'type': {'str'}},
             {'file': 'case15.py', 'line_number': 12, 'variable': 'x', 'function': 'my_function', 'type': 'str'}]
        )

    def test_case_16(self):
        inferrer = TypeInference(name='case16', entry_point='basecase/case16')
        inferrer.infer_types()
        inferred = inferrer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'file2.py', 'line_number': 1, 'function': 'imported_function', 'type': {'Tuple[str]'}},
             {'file': 'file2.py', 'line_number': 2, 'variable': 'return_value', 'function': 'imported_function',
              'type': 'Tuple[str]'},
             {'file': 'file1.py', 'line_number': 7, 'function': 'class_method', 'type': {'Tuple[str]'}},
             {'file': 'file1.py', 'line_number': 7, 'function': 'MyClass.class_method', 'type': {'Tuple[str]'}}]
        )

    def test_case_17(self):
        inferrer = TypeInference(name='case17', entry_point='basecase/case17.py')
        inferrer.infer_types()
        inferred = inferrer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case17.py', 'line_number': 5, 'function': 'fun2', 'type': {'float'}},
             {'file': 'case17.py', 'line_number': 1, 'parameter': 'a', 'function': 'fun1', 'type': 'float'},
             {'file': 'case17.py', 'line_number': 5, 'parameter': 'a', 'function': 'fun2', 'type': 'float'}]
        )

    def test_case_18(self):
        inferrer = TypeInference(name='case18', entry_point='basecase/case18.py')
        inferrer.infer_types()
        inferred = inferrer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case18.py', 'line_number': 5, 'function': 'MyParentClass.my_function', 'type': {'str'}},
             {'file': 'case18.py', 'line_number': 11, 'function': 'ChildClass.my_function', 'type': {'List[str]'}}]
        )

    def test_case_19(self):
        inferrer = TypeInference(name='case18', entry_point='basecase/case19.py')
        inferrer.infer_types()
        inferred = inferrer.get_types()
        self.assertEqual(
            inferred,
            []
        )

    def test_case_20(self):
        inferrer = TypeInference(name='case20', entry_point='basecase/case20.py')
        inferrer.infer_types()
        inferred = inferrer.get_types()
        self.assertEqual(
            inferred,
            [{'file': 'case20.py', 'line_number': 1, 'function': 'add', 'type': {'Union[str, int]'}},
             {'file': 'case20.py', 'line_number': 1, 'parameter': 'x', 'function': 'add', 'type': 'Union[str, int]'},
             {'file': 'case20.py', 'line_number': 1, 'parameter': 'y', 'function': 'add', 'type': 'Union[str, int]'}]
        )


if __name__ == '__main__':
    unittest.main()
